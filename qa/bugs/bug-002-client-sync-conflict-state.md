# Bug ID: BUG-002 - Client Sync Shows Success After Conflict

**Severity:** S4 - Minor  
**Environment:** Staging - Desktop sync client 3.4.1 / macOS 14

## Description
When a file sync conflict occurs, the client UI briefly shows "Sync Complete" before displaying the conflict icon, causing users to assume data is current.

## Steps to Reproduce
1. Edit the same document from two clients while offline.
2. Reconnect both clients to the network.
3. Wait for automatic sync reconciliation.
4. Observe status banner and sync history.

## Expected Result
Client should display a conflict warning immediately and suppress success messaging until conflict resolution is complete.

## Actual Result
Client shows "Sync Complete" for several seconds, then transitions to conflict state.

## Evidence
- Sanitized client log excerpt: `sync_result=conflict` arrives after UI success event is emitted.

## Impact
Temporary success signal creates user confusion and increases duplicate tickets for suspected data-loss incidents.
