-- 1a. Display the first and last names of all actors from the table actor.
SELECT first_name, last_name FROM actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT *,CONCAT(first_name, ' ',last_name) as `Actor Name`
FROM actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'JOE';

-- 2b. Find all actors whose last name contain the letters GEN:
SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name LIKE '%GEN%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name LIKE '%LI%'
ORDER BY
 last_name ASC,
 first_name ASC;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
ALTER TABLE actor ADD COLUMN description BLOB;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE actor DROP COLUMN description;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name,
COUNT(last_name)
AS total
FROM actor
GROUP BY last_name
ORDER BY last_name ASC;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT * 
FROM
(
SELECT last_name,
COUNT(last_name)
AS total
FROM actor
GROUP BY last_name
ORDER BY last_name ASC
)
AS a
WHERE total >= 2;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
UPDATE actor
 SET first_name = replace(first_name, 'GROUCHO', 'HARPO')
 WHERE last_name = 'WILLIAMS';
 
-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
UPDATE actor
 SET first_name = replace(first_name, 'HARPO', 'GROUCHO')
 WHERE last_name = 'WILLIAMS';
 
-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT staff.first_name, staff.last_name, address.address
FROM staff
JOIN address
ON staff.address_id = address.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
SELECT staff.first_name, staff.last_name, a.total FROM
	(
	SELECT staff_id,
	SUM(amount)
	AS total
	FROM payment
    WHERE payment_date BETWEEN '2005-08-01 00:00:00' and '2005-08-31 23:59:59' 
	GROUP BY staff_id
	)
	AS a
JOIN
	staff
ON a.staff_id = staff.staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT film.title, a.actor_number FROM
	(
	SELECT film_id,
	COUNT(film_id) as actor_number
	FROM film_actor
	GROUP BY film_id
	)
	AS a
JOIN
	film
ON a.film_id = film.film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT film.title, a.film_number
	FROM
	(
	SELECT film_id,
	COUNT(film_id) as film_number
	FROM inventory
	GROUP BY film_id
	)
	AS a
JOIN
	film
ON a.film_id = film.film_id
WHERE title = 'HUNCHBACK IMPOSSIBLE';

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT customer.first_name, customer.last_name, a.total FROM
	(
	SELECT customer_id,
	SUM(amount)
	AS total
	FROM payment
	GROUP BY customer_id
	)
	AS a
JOIN
	customer
ON a.customer_id = customer.customer_id
ORDER BY last_name ASC;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT film.title
FROM film
WHERE language_id = 
(
	SELECT language_id
	FROM `language`
	WHERE `name` = "English"
)
AND title LIKE "K%" OR title LIKE "Q%";

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT actor.first_name, actor.last_name
FROM actor
WHERE actor_id IN
(
	SELECT actor_id
	FROM film_actor
	WHERE film_id = 
	(
		SELECT film_id
		FROM film
		WHERE title = "ALONE TRIP"
	)
);

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT customer.first_name, customer.last_name, customer.email
FROM customer
JOIN address
ON customer.address_id = address.address_id
JOIN city
ON address.city_id = city.city_id
JOIN country
ON city.country_id = country.country_id
WHERE country = "Canada";

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT film.title
FROM film
JOIN film_category
ON film.film_id = film_category.film_id
JOIN category
ON film_category.category_id = category.category_id
WHERE `name` = "Family";

-- 7e. Display the most frequently rented movies in descending order.
SELECT title, film_count
FROM
(
	SELECT *,
	SUM(inventory_count) as film_count
	FROM
	(
		SELECT film_id, inventory_count
		FROM
		(
			SELECT inventory_id,
			COUNT(inventory_id) AS inventory_count
			FROM rental
			GROUP BY inventory_id
		)
		AS a
		JOIN inventory
		ON a.inventory_id = inventory.inventory_id
	)
	AS b
	GROUP BY film_id
)
AS c
JOIN film
ON c.film_id = film.film_id
ORDER BY film_count DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT store_id, store_total
FROM
(
	SELECT *,
	SUM(total) AS store_total
	FROM
		(
		SELECT store_id, total
		FROM
			(
			SELECT *,
			SUM(amount) as total
			FROM payment
			GROUP BY customer_id
			)
		AS a
		JOIN customer
		ON a.customer_id = customer.customer_id
		)
	AS b
	GROUP BY store_id
)
AS c
;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT store_id, city, country
FROM
(
SELECT store_id, city, country_id
FROM
(
SELECT store_id, address, city_id
FROM store
JOIN address
ON store.address_id = address.address_id
)
AS a
JOIN city
ON a.city_id = city.city_id
)
AS b
JOIN country
ON b.country_id = country.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT `name`, Total
FROM
(
SELECT *,
SUM(amount) as Total
FROM
(
SELECT name, amount
FROM
(
SELECT category_id, amount
FROM
(
SELECT film_id, amount
FROM
(
SELECT inventory_id, amount
FROM payment
JOIN rental
ON payment.rental_id = rental.rental_id
)
AS a
JOIN inventory
ON a.inventory_id = inventory.inventory_id
)
AS b
JOIN film_category
ON b.film_id = film_category.film_id
)
AS c
JOIN category
ON c.category_id = category.category_id
)
AS d
GROUP BY `name`
)
AS e
ORDER by Total DESC
LIMIT 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW Top_5_Genres AS
(
SELECT `name`, Total
FROM
(
SELECT *,
SUM(amount) as Total
FROM
(
SELECT name, amount
FROM
(
SELECT category_id, amount
FROM
(
SELECT film_id, amount
FROM
(
SELECT inventory_id, amount
FROM payment
JOIN rental
ON payment.rental_id = rental.rental_id
)
AS a
JOIN inventory
ON a.inventory_id = inventory.inventory_id
)
AS b
JOIN film_category
ON b.film_id = film_category.film_id
)
AS c
JOIN category
ON c.category_id = category.category_id
)
AS d
GROUP BY `name`
)
AS e
ORDER by Total DESC
LIMIT 5
);

-- 8b. How would you display the view that you created in 8a?
SELECT * FROM top_5_genres;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW top_5_genres;