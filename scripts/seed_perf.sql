-- Load-test data: 2,000 authors, 800,000 books. Run against the DEV database only.
TRUNCATE books, authors RESTART IDENTITY CASCADE;
INSERT INTO authors (name, country)
SELECT 'Author ' || g, (ARRAY['Nigeria','USA','Japan','UK','Ghana'])[1 + g % 5]
FROM generate_series(1, 2000) g;
INSERT INTO books (title, author_id, price, in_stock)
SELECT CASE WHEN g % 2000 = 7 THEN 'Zephyr ' ELSE '' END
       || (ARRAY['Dune','Beloved','Kafka','Sula','Night','River','Silent','Golden','Iron','Paper'])[1 + g % 10]
       || ' ' || (ARRAY['Garden','Empire','Shore','Song','Road','House','Tide','Crown'])[1 + (g / 10) % 8]
       || ' ' || g,
       1 + g % 2000,
       round((random() * 99 + 1)::numeric, 2),
       random() < 0.9
FROM generate_series(1, 800000) g;
VACUUM ANALYZE authors;
VACUUM ANALYZE books;
