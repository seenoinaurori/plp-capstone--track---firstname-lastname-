-- 1. What are the H1 2026 headline KPIs?
SELECT COUNT(*) AS order_count,
       SUM(revenue) AS revenue_kes,
       SUM(revenue) / COUNT(DISTINCT order_id) AS average_order_value_kes
FROM sales;

-- 2. Which branches exceed KES 5 million in revenue?
SELECT branch, COUNT(*) AS orders, SUM(revenue) AS revenue_kes
FROM sales
GROUP BY branch
HAVING SUM(revenue) > 5000000
ORDER BY revenue_kes DESC;

-- 3. Which products generate the most revenue within each category? (window)
WITH product_sales AS (
    SELECT category, product, SUM(revenue) AS revenue_kes
    FROM sales
    GROUP BY category, product
)
SELECT category, product, revenue_kes,
       RANK() OVER (PARTITION BY category ORDER BY revenue_kes DESC) AS category_rank
FROM product_sales
ORDER BY category, category_rank;

-- 4. How do channel-level basket sizes compare by branch? (JOIN)
WITH branch_channel AS (
    SELECT branch, channel, COUNT(*) AS orders, SUM(revenue) AS revenue_kes
    FROM sales
    GROUP BY branch, channel
)
SELECT a.branch, a.orders AS online_orders, a.revenue_kes AS online_revenue_kes,
       b.orders AS store_orders, b.revenue_kes AS store_revenue_kes
FROM branch_channel AS a
JOIN branch_channel AS b ON a.branch = b.branch
WHERE a.channel = 'Online' AND b.channel = 'In-store'
ORDER BY a.branch;

-- 5. What is the month-to-month revenue movement?
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(revenue) AS revenue_kes
    FROM sales
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, revenue_kes,
       revenue_kes - LAG(revenue_kes) OVER (ORDER BY month) AS change_vs_prior_month_kes
FROM monthly
ORDER BY month;

-- 6. Which branch and category combinations are largest?
SELECT branch, category, COUNT(*) AS orders, SUM(revenue) AS revenue_kes
FROM sales
GROUP BY branch, category
ORDER BY revenue_kes DESC;
