-- Lukuoikeudet liikennekantaan scripts/paivita_suosio.py:tä varten.
--
-- Aja tämä adminina siinä kannassa jossa faktataulu on. Korvaa <kanta> ja
-- <skeema> omillasi; jos skeemoja on useampi, toista USAGE- ja SELECT-rivit
-- kullekin. Vaihda salasana ennen ajoa.
--
-- Tunnus on tarkoituksella hyödytön kaikkeen muuhun kuin lukemiseen: se ei voi
-- kirjoittaa, sen kyselyt katkeavat 30 sekunnissa eikä se voi avata kuin kolme
-- yhtäaikaista yhteyttä. Yöajo tarvitsee yhden.

CREATE ROLE ilmiot_lukija LOGIN PASSWORD 'VAIHDA-TAMA';

GRANT CONNECT ON DATABASE <kanta>  TO ilmiot_lukija;
GRANT USAGE   ON SCHEMA   <skeema> TO ilmiot_lukija;
GRANT SELECT  ON ALL TABLES IN SCHEMA <skeema> TO ilmiot_lukija;

-- Myös taulut jotka luodaan myöhemmin, jottei tunnus hajoa seuraavassa
-- mallin muutoksessa
ALTER DEFAULT PRIVILEGES IN SCHEMA <skeema>
  GRANT SELECT ON TABLES TO ilmiot_lukija;

-- Vyö ja henkselit: vaikka jokin grantti annettaisiin vahingossa, istunto on
-- silti vain luku -tilassa
ALTER ROLE ilmiot_lukija SET default_transaction_read_only = on;
ALTER ROLE ilmiot_lukija SET statement_timeout = '30s';
ALTER ROLE ilmiot_lukija SET idle_in_transaction_session_timeout = '60s';
ALTER ROLE ilmiot_lukija CONNECTION LIMIT 3;

-- Ei oikeutta luoda mitään public-skeemaan (PG 15+ tekee tämän jo itse)
REVOKE CREATE ON SCHEMA public FROM ilmiot_lukija;
REVOKE ALL ON DATABASE <kanta> FROM PUBLIC;


-- ── pg_hba.conf ────────────────────────────────────────────────────────
-- Lisää rivi sille verkolle josta skripti ajetaan, ennen laveampia sääntöjä.
-- Rajaa isäntä tai aliverkko, älä avaa 0.0.0.0/0.
--
--   host    <kanta>    ilmiot_lukija    <wsl-aliverkko>/24    scram-sha-256
--
-- Ja lataa asetukset uudelleen ilman uudelleenkäynnistystä:
--
--   SELECT pg_reload_conf();


-- ── Tarkistus ──────────────────────────────────────────────────────────
-- Tämän pitää onnistua:
--   python3 scripts/paivita_suosio.py --skeema
--
-- Ja tämän pitää epäonnistua (oikeuksien varmistus):
--   CREATE TABLE koe (x int);   -->  ERROR: cannot execute CREATE TABLE in a
--                                    read-only transaction
