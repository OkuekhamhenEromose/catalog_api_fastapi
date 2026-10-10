\echo === Q1: in-stock books priced 10.00-10.10, sorted by price (page 1) ===
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT id, title, price FROM books
WHERE in_stock = true AND price >= 10 AND price <= 10.10
ORDER BY price ASC, id ASC LIMIT 20 OFFSET 0;
\echo === Q2: title search 'zephyr' (page 1) ===
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT id, title FROM books WHERE title ILIKE '%zephyr%' ORDER BY id ASC LIMIT 20;
\echo === Q3: books of one author (page 1) ===
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT id, title FROM books WHERE author_id = 777 ORDER BY id ASC LIMIT 20;
\echo === Q4: total for Q1 filter ===
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT count(*) FROM books WHERE in_stock = true AND price >= 10 AND price <= 10.10;
\echo === Q5: title search with NO matches ('xyzzy') - the worst case ===
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT id, title FROM books WHERE title ILIKE '%xyzzy%' ORDER BY id ASC LIMIT 20;
