-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports WHERE street LIKE 'Humphrey Street' AND year = 2021 AND month = 7 AND day = 28;
-- 10:15am
-- three witnesses
-- bakery

SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- Emma's bakery
-- ATM on Leggett Street and saw the thief there withdrawing some money.
-- I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.

SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE 'Leggett Street' AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw');
--  +-----------+
-- | person_id |
-- +-----------+
-- | 686048    |
-- | 514354    |
-- | 458378    |
-- | 395717    |
-- | 396669    |
-- | 467400    |
-- | 449774    |
-- | 438727    |
-- +-----------+

SELECT license_plate FROM bakery_security_logs WHERE (year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND (minute BETWEEN 15 AND 25) AND activity = 'exit');
-- +---------------+
-- | license_plate |
-- +---------------+
-- | 5P2BI95       |
-- | 94KL13X       |
-- | 6P58WS2       |
-- | 4328GD8       |
-- | G412CB7       |
-- | L93JTIZ       |
-- | 322W7JE       |
-- | 0NTHK55       |
-- +---------------+

SELECT id FROM airports WHERE city LIKE 'Fiftyville';
-- +----+
-- | id |
-- +----+
-- | 8  |
-- +----+

SELECT id, destination_airport_id FROM flights WHERE (origin_airport_id = 8 AND year = 2021 AND month = 7 AND day = 29) ORDER BY hour, minute LIMIT 1;
-- +----+------------------------+
-- | id | destination_airport_id |
-- +----+------------------------+
-- | 36 | 4                      |
-- +----+------------------------+

SELECT full_name, abbreviation, city FROM airports WHERE id = 4;
-- +-------------------+--------------+---------------+
-- |     full_name     | abbreviation |     city      |
-- +-------------------+--------------+---------------+
-- | LaGuardia Airport | LGA          | New York City |
-- +-------------------+--------------+---------------+

SELECT id, name FROM people
WHERE phone_number IN (SELECT caller FROM phone_calls WHERE (year = 2021 AND month = 7 AND day = 28) AND duration < 60)
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE (year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND (minute BETWEEN 15 AND 25) AND activity = 'exit'))
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE 'Leggett Street' AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw'));
-- +--------+-------+
-- |   id   | name  |
-- +--------+-------+
-- | 686048 | Bruce |
-- +--------+-------+

SELECT name, phone_number FROM people WHERE id = 686048;
-- +-------+----------------+
-- | name  |  phone_number  |
-- +-------+----------------+
-- | Bruce | (367) 555-5533 |
-- +-------+----------------+

SELECT id, name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = '(367) 555-5533' AND (year = 2021 AND month = 7 AND day = 28));
-- +--------+-------+
-- |   id   | name  |
-- +--------+-------+
-- | 864400 | Robin |
-- +--------+-------+
