# Knowledge Base Sources — Digital Arrest Scam Shield

Tracks the ~15 reference documents for the RAG knowledge base. We do **not**
fabricate official advisory text — every file dropped in `documents/raw/`
must be either:
(a) downloaded directly from the official source listed below, or
(b) a clearly-labeled placeholder/summary written by us for testing only.

| # | Category | Trusted Source | Status |
|---|---|---|---|
| 1 | Digital arrest scams — general awareness | cybercrime.gov.in (I4C advisories) | placeholder — replace with real PDF |
| 2 | Digital arrest scams — MHA press note | pib.gov.in (Ministry of Home Affairs releases) | placeholder |
| 3 | UPI fraud awareness | rbi.org.in (RBI consumer awareness) | placeholder |
| 4 | Online banking scams | rbi.org.in | placeholder |
| 5 | Phishing awareness | cert-in.org.in | placeholder |
| 6 | OTP scam awareness | cert-in.org.in | placeholder |
| 7 | FICN (fake currency) advisory | rbi.org.in Annual Report | placeholder |
| 8 | Reporting process — NCRB | cybercrime.gov.in | placeholder |
| 9 | Spoofed call / number awareness | trai.gov.in | placeholder |
| 10 | Courier/parcel scam (common digital-arrest pretext) | cybercrime.gov.in | placeholder |
| 11 | Fake government portal awareness | cert-in.org.in | placeholder |
| 12 | Video-call impersonation scam pattern | press coverage (The Hindu / Indian Express, factual reporting only) | placeholder |
| 13 | Money mule account awareness | RBI / cybercrime.gov.in | placeholder |
| 14 | Senior citizen targeted scam advisory | cybercrime.gov.in | placeholder |
| 15 | General digital safety checklist | cert-in.org.in | placeholder |

## Rules for adding real documents
1. Download the PDF/text directly from the `.gov.in` source listed above.
2. Drop it in `documents/raw/` with a descriptive filename, e.g. `cert-in_otp-scam-advisory.pdf`.
3. Update the table above: change status from `placeholder` to `added (<date>)`.
4. Never copy-paste large blocks of advisory text into our own files and claim it as original — link/cite the source, don't reproduce wholesale.
5. Run `python -m src.ingestion.ingest` after adding new docs to rebuild the vector store.

## Day 1 placeholder files
For testing the pipeline today, `documents/raw/` contains short, clearly-labeled
`SAMPLE — not official` `.txt` files per category so ingestion/retrieval can be
verified end-to-end before real advisories are sourced.
