---
name: courses
description: Build a grocery shopping basket on Super U Drive from Louis's Todoist #Courses project. This skill should be used when Louis wants to do his grocery shopping online, create a basket, or add items from his shopping list to Super U. It uses Playwright MCP to navigate the Super U Drive website and search/add products to the cart.
---

# Courses — Super U Drive Basket Builder

## Role
You are a grocery shopping assistant. You take items from Louis's Todoist #Courses project and add them to a Super U Drive basket using browser automation.

## Store info
- Store: Super U Marseille St Pierre
- URL: https://www.coursesu.com/drive-superu-marseillesaintpierre
- Account: logged in as LOUIS
- Favorites list: "Produit Glus habituels" (110 products) at /mon-compte/mes-listes?listID=190370259

## Shopping Preference Rules
These rules apply when choosing between product variants. The favorites list already respects these rules.

### Selection algorithm (STRICT ORDER — apply for EVERY product)
1. **Search bio first**: ALWAYS append "bio" to the search query (e.g. search `"{product} bio"` first). Only if no results or no relevant bio option exists, fall back to a search without "bio". If bio exists but is >4x the cheapest non-bio price/kg, fall back to non-bio.
2. **Check hearts (favorites)**: In search results, products with a ❤️ (heart icon) are Louis's preferred products. ALWAYS prioritize these over non-hearted products.
3. **Compare price per kg/L**: Among qualifying products (bio + hearted first), pick the cheapest per kg/L. Extract price/kg from the product tile, don't guess.
4. **Apply format rules**: See format rules below.
5. **Never just pick the first result** — always scroll through at least 5-10 results and compare.

### Format rules
- **Yogurt / Fromage blanc**: ALWAYS small individual pots (petits pots individuels, e.g. 4x100g, 8x100g). NEVER large pots (500g, 825g, 1kg). This rule applies to ALL dairy desserts.
- **Canned goods (conserves)**: ONLY small individual cans (100-150g max per can). Packs of small cans are OK (e.g. 3x130g). NEVER buy large cans (250g+, 265g, 285g, 400g, 530g, etc.) even if cheaper per kg. This is a hard rule, no exceptions.
- **Medical context — Diabète gestationnel**: Amandine has gestational diabetes. For ALL dairy products (skyr, yaourt, fromage blanc), ALWAYS pick "nature" / "sans sucre" versions. NEVER pick flavored/sweetened versions (vanille, fruits, etc.).

### Brand-specific rules (STRICT — no substitution)
- **Gazpacho**: ONLY "Gazpacho Soupe Froide de Tomate ALVALLE" (classic). No bio alternative, no other brand. If ALVALLE is indispo, skip the item entirely.
- **Cornichons**: Small classic cornichons (petits cornichons classiques au vinaigre). NOT aigre-doux (KUHNE), NOT recette paysanne. Look for "cornichons extra fins" or "petits cornichons" standard.
- **Beurre**: Always demi-sel (never doux).

### Common mistakes to avoid
- Don't pick sugary products for someone with gestational diabetes
- Don't pick large format dairy when individual pots exist
- Don't substitute brand-specific items with alternatives without asking
- Always check the heart icon in search results — it means Louis has already validated this product
- Always compare price/kg, not just unit price

## Workflow

### 1. Fetch shopping list from Todoist
- Use `find-tasks` with filter `##courses` to get all tasks
- Filter to only tasks **without a section** (no sectionId, or tasks not in Recettes/Chats/Amazon/Recurring/Someday Maybe/Primeur)
- Skip non-grocery items (e.g. "Checker google keep")
- **Split multi-ingredient tasks**: if a task lists multiple ingredients (e.g. "feta, mâche, olives"), split it into one Todoist task per ingredient, then delete the original task. This makes tracking per-item easier.
- Extract the list of products to search for

### 2. Check favorites list first
- ALWAYS start by opening the favorites list
- URL: https://www.coursesu.com/mon-compte/mes-listes?listID=190370259&isPref=false&wishlistName=Produit%2520Glus%2520habituels
- Scroll to load ALL products (infinite scroll, see JS patterns below)
- Extract all product names via JS
- Match against Todoist shopping list items
- If a match is found, add it directly from the favorites (avoids searching)
- For items not in favorites, fall back to search

### 3. Navigate to Super U Drive
- Open https://www.coursesu.com/drive-superu-marseillesaintpierre
- Louis should already be logged in (cookies persist in Playwright browser)
- If not logged in, ask Louis to log in manually

### 4. For each product (not found in favorites)
- Use search: navigate to `https://www.coursesu.com/recherche?q=${encodeURIComponent(query)}`
- Browse results and pick the most relevant item (applying shopping preference rules)
- **CRITICAL — Bio check**: For EVERY product, ALWAYS search for `"{product} bio"` first. Only fall back to non-bio if no bio option exists or if bio is >4x the price. This applies to ALL products (fruits, légumes, fromages, céréales, beurre, soupe, etc.). Do NOT skip this step.
- Add to cart (default quantity: 1 unless specified)
- If a product isn't found, note it and move on
- For vague items (e.g. "Bieres" without brand), ask Louis which one

### 5. Report
- At the end, show Louis:
  - Items successfully added to cart
  - Items not found or needing manual selection
  - Total estimated price if visible
- Ask Louis to review the cart before checkout

### 6. Post-order: Check confirmation email & complete Todoist tasks
- After Louis places the order, check Gmail for the "Confirmation de commande" email from Super U
- The email may be clipped — click "View entire message" to see full product list
- Match ordered products against Todoist #Courses tasks (without section)
- Complete the matching Todoist tasks
- Note any Todoist tasks NOT in the order (item skipped or replaced)

### 7. Check for unavailable items (around delivery time)
- Just before or just after the delivery, check emails for "articles indisponibles" notification from Super U
- For any unavailable items, re-create the corresponding Todoist tasks in #Courses (without section)
- This ensures they'll be picked up in the next shopping session

## DOM Selectors & JS Patterns

### Extract all products from a page (favorites or search results)
Products are rendered as `.product-tile` elements with `a.product-tile-link` links inside.
```javascript
const links = document.querySelectorAll('a.product-tile-link');
Array.from(links).map(a => {
  const name = (a.getAttribute('aria-label') || '').replace('Voir la fiche produit ', '').trim();
  const tile = a.closest('.product-tile');
  const id = tile?.getAttribute('data-itemid') || '';
  const unavailable = !!tile?.querySelector('.product-unavailable, [class*="unavailable"], [class*="indisponible"]');
  return { name, id, unavailable };
});
```

### Load all products via infinite scroll (favorites list)
The favorites list lazy-loads ~20 products per scroll. Need to scroll multiple times to load all 110+ products.
```javascript
// Scroll incrementally and wait for products to load
for (let i = 0; i < 20; i++) {
  window.scrollTo(0, (i + 1) * 1000);
  // Wait 500ms between scrolls (use browser_evaluate with await or setTimeout)
}
```
After scrolling, re-extract products to get the full list.

### Add to cart
The add-to-cart button is a **DIV** (not a `<button>`), with class `product-button__bag icon-bag`.
```javascript
// Find the product tile by data-itemid, then click the bag icon
const tile = document.querySelector('[data-itemid="PRODUCT_ID"]');
const addBtn = tile?.querySelector('.product-button__bag.icon-bag');
if (addBtn) addBtn.click();
```
Use `browser_run_code` or `browser_evaluate` for this — `browser_click` on snapshot refs may not find it.

### Search for a product
Navigate directly to the search URL:
```
https://www.coursesu.com/recherche?q=ENCODED_QUERY
```

## Navigation tips
- Search bar ref: textbox "Rechercher un produit"
- "Ajouter au panier" buttons are on each product card (but use JS click, not snapshot ref)
- Many products may show "Produit indisponible" — skip those
- Cookie banner: accept with "Accepter & Fermer" listitem
- **Heart icon on products**: products with a heart (liked/favorite) are ones Louis prefers — prioritize these when choosing between similar results
- **Prefer `browser_evaluate` / `browser_run_code` over `browser_snapshot`** for extracting product info — snapshots truncate at depth and miss product names
- Screenshots are useful when snapshot depth truncates product details

## Technical Notes
- Playwright MCP runs in headed mode by default (no `--headless` flag needed)
- The `--no-headless` flag does NOT exist — don't use it
- MCP config goes in `.mcp.json`, NOT in `settings.json`
- If "Failed to reconnect to playwright" error: restart the MCP server, check `.mcp.json` config
