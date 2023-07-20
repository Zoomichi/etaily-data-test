-- 1)
SELECT * FROM customer WHERE gender = "female";

-- 2)
SELECT C.first_name, C.last_name, COUNT(O.id)
FROM customer C
LEFT JOIN order O
ON C.id = O.fk_customer
GROUP BY C.id;

-- 3)
SELECT C.first_name, C.last_name, SUM(O.sum)
FROM customer C
INNER JOIN order O
ON C.id = O.fk_customer
GROUP BY C.id;

-- 4)
SELECT order_nr
FROM order
WHERE id IN (
    SELECT fk_order
    FROM order_item
    GROUP BY fk_order
    HAVING COUNT(id) > 1
);