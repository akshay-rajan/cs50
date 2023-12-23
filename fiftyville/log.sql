-- Get the crime scene report of the crime
SELECT description
     FROM crime_scene_reports
    WHERE year = 2021
      AND month = 7
      AND day = 28
      AND street = "Humphrey Street";

--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses (all mentioned 'bakery')

--Get the details of the interviews conducted
SELECT name, transcript
     FROM interviews
    WHERE year = 2021
      AND month = 7
      AND day = 28
      AND transcript LIKE "%bakery%";

-- At morning, thief withdrew money from the ATM  on Legget Street. At 10:15, the theft occurs. After that, thief makes a phone call with apprentice,
-- which lasted less than a minute in which they decide to leave from Fiftyville on the first flight at 29-07-2021.
-- Thief gets into a car and leaves the bakery(10:15 - 10:25)

--Check security footage of bakery parking lot to obtain license plates: From 10:15 to 10:25, exit
SELECT license_plate
     FROM bakery_security_logs
    WHERE year = 2021
      AND month = 7
      AND day = 28
      AND hour = 10
      AND minute BETWEEN 15 AND 25
      AND activity = "exit";

-- Check the atm transactions to get the account numbers: July 28, 2021 morning, at Leggett Street, withdraw
SELECT account_number
     FROM atm_transactions
    WHERE year = 2021
      AND month = 7
      AND day = 28
      AND atm_location = "Leggett Street"
      AND transaction_type = "withdraw";

-- Check the call logs: After 10:15, <1m
SELECT caller, receiver
     FROM phone_calls
    WHERE year = 2021
      AND month = 7
      AND day = 28
      AND duration < 60;

--Check flight details: Earliest, July 29, 2021
SELECT city
     FROM airports
    WHERE id = (SELECT destination_airport_id
                    FROM flights
                    JOIN airports ON flights.origin_airport_id = airports.id
                    WHERE airports.city = "Fiftyville"
                    AND flights.year = 2021
                    AND flights.month = 7
                    AND flights.day = 29
                    ORDER BY flights.hour, flights.minute
                    LIMIT 1);

-- The thief escaped to New York City

SELECT passport_number
     FROM passengers
    WHERE flight_id = (SELECT flights.id
                              FROM flights
                              JOIN airports ON flights.origin_airport_id = airports.id
                              WHERE airports.city = "Fiftyville"
                              AND flights.year = 2021
                              AND flights.month = 7
                              AND flights.day = 29
                              ORDER BY flights.hour, flights.minute
                              LIMIT 1);

-- Find the matching person with license plates, passport numbers, bank accounts and phone numbers
SELECT name AS thief
     FROM people
          JOIN bank_accounts ON people.id = bank_accounts.person_id
    WHERE license_plate IN (SELECT license_plate
                              FROM bakery_security_logs
                         WHERE year = 2021
                              AND month = 7
                              AND day = 28
                              AND hour = 10
                              AND minute BETWEEN 15 AND 25
                              AND activity = "exit")
      AND passport_number IN (SELECT passport_number
                                   FROM passengers
                                   WHERE flight_id = (SELECT flights.id
                                                            FROM flights
                                                            JOIN airports ON flights.origin_airport_id = airports.id
                                                            WHERE airports.city = "Fiftyville"
                                                            AND flights.year = 2021
                                                            AND flights.month = 7
                                                            AND flights.day = 29
                                                            ORDER BY flights.hour, flights.minute
                                                            LIMIT 1))
      AND phone_number IN (SELECT caller
                              FROM phone_calls
                              WHERE year = 2021
                              AND month = 7
                              AND day = 28
                              AND duration < 60)
     AND bank_accounts.account_number IN (SELECT account_number
                                                  FROM atm_transactions
                                                  WHERE year = 2021
                                                  AND month = 7
                                                  AND day = 28
                                                  AND atm_location = "Leggett Street"
                                                  AND transaction_type = "withdraw");

-- The thief is Bruce

-- Track the apprentice using the phone call
SELECT name AS apprentice
      FROM people
     WHERE phone_number = (SELECT phone_calls.receiver
                                   FROM phone_calls
                                   JOIN people ON phone_calls.caller = people.phone_number
                                   WHERE caller = (SELECT people.phone_number
                                                       FROM people
                                                       WHERE name = "Bruce"
                                                       AND phone_calls.year = 2021
                                                       AND phone_calls.month = 7
                                                       AND phone_calls.day = 28
                                                       AND phone_calls.duration < 60));

-- The apprentice is Robin