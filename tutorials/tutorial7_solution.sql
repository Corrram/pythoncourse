/* ============================================================
   Tutorial 7 – SQL (music.db)

   Exercise 1–2: DQL (Data Query Language)
      - SELECT with WHERE, LIKE, IN, BETWEEN, DISTINCT
      - JOINs, GROUP BY, HAVING, ORDER BY, LIMIT
      - Subqueries, CTEs

   Exercise 3–5: Non-DQL (DDL, DML, TCL)
      - DDL: CREATE TABLE, CREATE VIEW, DROP
      - DML: INSERT, UPDATE, DELETE
      - TCL: BEGIN TRANSACTION, COMMIT, ROLLBACK
   ============================================================ */


-- ============================================================
-- Exercise 1 (DQL – Basic Filtering)
-- ============================================================

-- Q1: List all customers who live in Brazil, showing their name, city and country.
SELECT FirstName, LastName, City, Country
FROM customers
WHERE Country = 'Brazil';

-- Q2: Find all tracks with the word 'Love' in their name.
SELECT *
FROM tracks
WHERE Name LIKE '%Love%';

-- Q3: Find all albums whose name consists of more than one word.
SELECT *
FROM albums
WHERE title LIKE '% %';
--% % 是通配符，表示名称中间有空格，从而表示多于一个单词。

-- Q4: List all distinct billing countries on invoices (alphabetically).
SELECT DISTINCT BillingCountry --select后面加distinct表示只选择不重复的值
FROM invoices
ORDER BY BillingCountry; --order by表示排序 billingcountry表示按国家名排序

-- Q5: List all tracks whose media type is either MPEG audio file or AAC audio file.
SELECT t.TrackId, t.Name, mt.Name AS MediaType --选择曲目ID，曲目名称，媒体类型名称
--t.TrackId表示曲目ID，t.Name表示曲目名称，mt.Name表示媒体类型名称，
--t的意思是tracks表，mt的意思是media_types表，as MediaType是给mt.Name起的别名
FROM tracks t --从tracks表中选择数据，起别名t
JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId 
--连接media_types表，起别名mt，连接条件是tracks表的MediaTypeId等于media_types表的MediaTypeId
--on后面是连接条件
WHERE mt.Name IN ('MPEG audio file', 'AAC audio file')--筛选条件是媒体类型名称在'MPEG audio file'和'AAC audio file'之中
ORDER BY t.Name;--按曲目名称排序

-- Q6: List all invoices issued in the year 2011 (inclusive), using BETWEEN.
SELECT InvoiceId, InvoiceDate, Total
FROM invoices
WHERE InvoiceDate BETWEEN '2011-01-01' AND '2011-12-31'
ORDER BY InvoiceDate, InvoiceId;


-- ============================================================
-- Exercise 2 (DQL – Joins, Aggregation, Subqueries/CTEs)
-- ============================================================

-- Q1: Find the 10 albums with the highest number of tracks, listing album title and track count.
SELECT al.AlbumId, al.Title, COUNT(t.TrackId) AS TrackCount
FROM albums al
JOIN tracks t ON t.AlbumId = al.AlbumId
GROUP BY al.AlbumId, al.Title--按专辑ID和标题分组
ORDER BY TrackCount DESC, al.Title --al.Title用于在TrackCount相同时进行次级排序
LIMIT 10;

-- Q2: For each sales support agent, determine how many customers they support.
SELECT e.EmployeeId,
       e.FirstName || ' ' || e.LastName AS EmployeeName,
       COUNT(c.CustomerId) AS CustomerCount
FROM employees e
LEFT JOIN customers c ON c.SupportRepId = e.EmployeeId
WHERE e.Title = 'Sales Support Agent'
GROUP BY e.EmployeeId, EmployeeName
ORDER BY CustomerCount DESC, EmployeeName;

-- Q3: Find the five tracks with the highest number of play history events.
SELECT t.TrackId, t.Name AS TrackName, COUNT(ph.PlayHistoryId) AS PlayCount
FROM tracks t
JOIN play_histories ph ON ph.TrackId = t.TrackId
GROUP BY t.TrackId, t.Name
ORDER BY PlayCount DESC, TrackName
LIMIT 5;

-- Q4: For each playlist, determine how many distinct artists appear via their tracks in that playlist.
SELECT p.PlaylistId, p.Name AS PlaylistName,
       COUNT(DISTINCT ar.ArtistId) AS ArtistCount
FROM playlists p
JOIN playlist_track pt ON pt.PlaylistId = p.PlaylistId
JOIN tracks t ON t.TrackId = pt.TrackId
JOIN albums al ON al.AlbumId = t.AlbumId
JOIN artists ar ON ar.ArtistId = al.ArtistId
GROUP BY p.PlaylistId, p.Name
ORDER BY ArtistCount DESC, PlaylistName;

-- Q5: List the top 5 customers who have spent the most money on music.
SELECT c.CustomerId,
       c.FirstName || ' ' || c.LastName AS CustomerName,
       SUM(ii.UnitPrice * ii.Quantity) AS TotalSpent
FROM customers c
JOIN invoices i USING (CustomerId)
JOIN invoice_items ii USING (InvoiceId)
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY TotalSpent DESC
LIMIT 5;

-- Q6: List all customers whose total spending is higher than the average total spending
-- across all customers (computed via a subquery).
SELECT c.CustomerId,
       c.FirstName || ' ' || c.LastName AS CustomerName,
       SUM(i.Total) AS TotalSpent
FROM customers c
JOIN invoices i ON i.CustomerId = c.CustomerId
GROUP BY c.CustomerId, CustomerName
HAVING SUM(i.Total) > (
    SELECT AVG(customer_total)
    FROM (
        SELECT SUM(Total) AS customer_total
        FROM invoices
        GROUP BY CustomerId
    )
)
ORDER BY TotalSpent DESC;

-- Q7: Find the most popular genre in terms of total sales using a CTE.
WITH GenreSales AS (
SELECT g.GenreId, g.Name AS GenreName, SUM(ii.UnitPrice * ii.Quantity) AS TotalSales
FROM tracks t
JOIN genres g USING (GenreId)
JOIN invoice_items ii USING (TrackId)
GROUP BY g.GenreId, g.Name
)
SELECT GenreId, GenreName, TotalSales
FROM GenreSales
ORDER BY TotalSales DESC
LIMIT 1;

-- Q8: Find "cross-platform hits": tracks that were played on at least 2 different device types
-- and purchased at least 2 times. Show track name, number of devices, play count and purchase count.
WITH play_stats AS (
  SELECT ph.TrackId,
         COUNT(*) AS PlayCount,
         COUNT(DISTINCT ph.Device) AS DeviceCount
  FROM play_histories ph
  GROUP BY ph.TrackId
),
purchase_stats AS (
  SELECT ii.TrackId,
         SUM(ii.Quantity) AS PurchaseCount
  FROM invoice_items ii
  GROUP BY ii.TrackId
)
SELECT t.TrackId, t.Name AS TrackName,
       ps.DeviceCount,
       ps.PlayCount,
       pu.PurchaseCount
FROM tracks t
JOIN play_stats ps ON ps.TrackId = t.TrackId
JOIN purchase_stats pu ON pu.TrackId = t.TrackId
WHERE ps.DeviceCount >= 2
  AND pu.PurchaseCount >= 2
ORDER BY pu.PurchaseCount DESC, ps.PlayCount DESC, TrackName;


-- ============================================================
-- Exercise 3 (DDL – Table and View Definitions)
-- ============================================================

-- Q1: Create a table to store how much employees like different genres (composite primary key).
CREATE TABLE IF NOT EXISTS genre_ratings (
    EmployeeId INTEGER NOT NULL,
    GenreId    INTEGER NOT NULL,
    Rating     INTEGER NOT NULL,
    PRIMARY KEY (EmployeeId, GenreId)
);

-- Q2: Create a view that shows all Rock tracks (track name, album title, artist name).
CREATE VIEW rock_tracks AS
SELECT t.TrackId,
       t.Name   AS TrackName,
       al.Title AS AlbumTitle,
       ar.Name  AS ArtistName
FROM tracks t
JOIN albums  al ON t.AlbumId  = al.AlbumId
JOIN artists ar ON al.ArtistId = ar.ArtistId
JOIN genres  g  ON t.GenreId  = g.GenreId
WHERE g.Name = 'Rock';


-- ============================================================
-- Exercise 4 (DML – Insert, Update, Delete)
-- ============================================================

-- Q1: Insert three example ratings for employee 1 into genre_ratings.
INSERT INTO genre_ratings (EmployeeId, GenreId, Rating)
VALUES
    (1, 1, 5),
    (1, 2, 4),
    (1, 3, 3);

-- Q2: Increase the rating for employee 1 and genre 3 to 4.
UPDATE genre_ratings
SET Rating = 4
WHERE EmployeeId = 1
  AND GenreId    = 3;

-- Q3: Delete the rating of employee 1 for genre 2 from genre_ratings.
DELETE FROM genre_ratings
WHERE EmployeeId = 1
  AND GenreId    = 2;

-- Q4: Remove all rows from genre_ratings, but keep the table definition.
DELETE FROM genre_ratings;

-- Q5: Drop the genre_ratings table completely.
DROP TABLE IF EXISTS genre_ratings;


-- ============================================================
-- Exercise 5 (TCL – Transactions)
-- ============================================================

-- Q1: Start a transaction that inserts two songs/soundtracks/... of your choice and then commits.
BEGIN TRANSACTION;

INSERT INTO tracks
    (Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
VALUES
    -- "I Don't Want to Set the World on Fire" – The Ink Spots
    ('I Don''t Want to Set the World on Fire',
     176,         -- Original Soundtracks 1
     1,       -- MPEG audio file
     10,          -- Soundtrack
     'Benjamin / Durham / Marcus / Seiler',
     178000,
     6820000,
     0.99),

    -- "Atom Bomb Baby" – The Five Stars
    ('Atom Bomb Baby',
     176,
     1,
     10,
     'John F. Young',
     136000,
     5300000,
     0.99);

COMMIT;


-- Q2: Start a transaction that inserts a new customer, then roll it back.
BEGIN TRANSACTION;

INSERT INTO customers
    (FirstName, LastName, Company, Address, City, State, Country,
     PostalCode, Phone, Fax, Email, SupportRepId)
VALUES
    ('John', 'Doe',
     'Data Science Student GmbH',
     'Freiburg Campus 1',
     'Freiburg', 'BW', 'Germany',
     '79098',
     '+49 761 1234567',
     NULL,
     'john.doe@student.uni-freiburg.de',
     3);

ROLLBACK;


/* ============================================================
   Additional Resources for SQL Practice
   ------------------------------------------------------------
   The following platforms can be used for further practice, ranging from
   beginner concepts to advanced data science interview preparation.

   Interactive Tutorials (Beginner to Intermediate)
      - SQLBolt (https://sqlbolt.com/)
        Short, interactive lessons to grasp and repeat the basics of SQL.
      - SQLZoo (https://sqlzoo.net/)
        Comprehensive, wiki-style resource; tutorials introduce new concepts.

   Structured Exercises (Intermediate)
      - SQL Practice (https://www.sql-practice.com/)
        Dedicated environment for running queries on sample datasets.
        Problems increase in difficulty to build muscle memory.

   Advanced Application (Analytics & Interview Prep)
      - DataLemur (https://datalemur.com/)
        Focuses on data analytics and business intelligence SQL questions.
        Features real-world interview questions.
      - StrataScratch (https://www.stratascratch.com/)
        Exercises geared toward data science and engineering roles.
        Provides access to complex corporate datasets.

   Note: Resources often offer a mix of free content and premium features,
   but the free tiers are usually sufficient for practice.
   ============================================================ */

