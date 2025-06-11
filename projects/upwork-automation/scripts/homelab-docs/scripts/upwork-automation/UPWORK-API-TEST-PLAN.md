# UPWORK AUTOMATION API TEST PLAN
**Date:** June 3, 2025  
**Version:** 1.0  
**Status:** ACTIVE  
**Environment:** Test API (Port 5052)

## Overview

This test plan outlines the strategy for testing the Upwork Automation API system in the test environment. The test environment has been set up according to the SAFE-API-IMPLEMENTATION-PLAN.md and is documented in TEST-API-SETUP-COMPLETE.md.

## Test Environment

- **Test API Server:** https://test-api.projekt-ai.net (Port 5052)
- **Test Pages Server:** https://test-pages.projekt-ai.net
- **Test API File:** `/root/homelab-docs/scripts/upwork-automation/api-server-test.py`
- **Proposal Queue:** `/root/homelab-docs/scripts/upwork-automation/proposal-queue.json`
- **Test Dashboard:** https://test-pages.projekt-ai.net/upwork-dashboard-test.html
- **API Test Page:** https://test-pages.projekt-ai.net/api-test-safe.html

## Test Categories

### 1. API Server Functionality

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|----------------|
| API-01 | Server Startup | Verify API server starts on port 5052 | Server starts without errors |
| API-02 | Health Endpoint | Test /api/health endpoint | Returns 200 OK with status "ok" |
| API-03 | Proposals Endpoint | Test /api/proposals endpoint | Returns 200 OK with valid proposals data |
| API-04 | CORS Headers | Check CORS headers in API responses | Appropriate CORS headers present |
| API-05 | Cache Control | Check cache control headers | No-cache headers present |
| API-06 | Error Handling | Test with invalid endpoints | Returns appropriate error codes |
| API-07 | Data Structure | Verify proposal data structure | JSON structure matches expected format |
| API-08 | Data Integrity | Verify proposal data contents | Proposal data is accurate and complete |

### 2. Dashboard Integration

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|----------------|
| DASH-01 | Dashboard Loading | Load test dashboard page | Page loads without errors |
| DASH-02 | API Connection | Verify dashboard connects to test API | Dashboard retrieves data from test API |
| DASH-03 | Proposal Display | Check proposals are displayed | Proposals are visible in the dashboard |
| DASH-04 | Proposal Filtering | Test proposal filtering functionality | Filtering works as expected |
| DASH-05 | Approve Button | Test approve button functionality | Button works and updates status |
| DASH-06 | Reject Button | Test reject button functionality | Button works and updates status |
| DASH-07 | View Proposal | Test view proposal button | Opens proposal in new tab |
| DASH-08 | Responsiveness | Test on different screen sizes | Dashboard is responsive |

### 3. Proposal Generation

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|----------------|
| GEN-01 | Job Processing | Process a test job via webhook | Job is processed successfully |
| GEN-02 | Score Calculation | Verify job scoring algorithm | Score is calculated correctly |
| GEN-03 | Template Application | Check proposal template application | Template is applied correctly |
| GEN-04 | File Generation | Verify HTML file creation | HTML file is created with correct content |
| GEN-05 | URL Formation | Check proposal URL format | URL follows the expected format |
| GEN-06 | Queue Update | Verify proposal queue update | Queue is updated with new proposal |

### 4. Security & Performance

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|----------------|
| SEC-01 | SSL Verification | Check HTTPS connection | SSL is configured correctly |
| SEC-02 | Headers Security | Verify security-related headers | Appropriate security headers present |
| SEC-03 | Access Control | Test unauthorized access attempts | Unauthorized access is prevented |
| PERF-01 | Response Time | Measure API response time | Response time under 500ms |
| PERF-02 | Load Testing | Test with multiple concurrent requests | API handles multiple requests |
| PERF-03 | Resource Usage | Monitor CPU and memory usage | Resource usage within acceptable limits |

## Test Scripts

The following test scripts have been created to automate the testing process:

1. **`test-api-endpoints.sh`** - Tests the API server functionality
   ```bash
   # Run from the scripts/upwork-automation directory
   ./test-api-endpoints.sh
   ```

2. **`test-dashboard-integration.sh`** - Tests the dashboard integration
   ```bash
   # Run from the scripts/upwork-automation directory
   ./test-dashboard-integration.sh
   ```

3. **`test-reject-endpoint.sh`** - Tests the reject functionality
   ```bash
   # Already exists, can be used for testing
   ./test-reject-endpoint.sh
   ```

## Manual Testing

Some aspects require manual testing in a browser:

1. Load the test dashboard: https://test-pages.projekt-ai.net/upwork-dashboard-test.html
2. Verify proposals are displayed correctly
3. Test the following buttons:
   - Approve button
   - Reject button
   - View Proposal button
   - Original Job Link button
4. Test filtering and sorting functionality
5. Verify responsive design by resizing the browser window

## Test Data

The tests should use the existing proposal data in the proposal-queue.json file. If needed, you can generate additional test data using the following methods:

1. **Manually craft test jobs:**
   ```json
   [{
       "title": "Test Job for API Testing",
       "budget": "$2,000",
       "description": "This is a test job for API testing purposes. We need an automation expert to help with our Make.com workflows.",
       "client": {
           "name": "Test Client",
           "paymentVerified": true
       },
       "link": "https://www.upwork.com/jobs/test-job"
   }]
   ```

2. **Use existing scripts:**
   ```bash
   # If existing test scripts are available
   python3 test_filtering_system.py
   ```

## Test Execution Sequence

1. Run API endpoint tests to verify the API server is functioning correctly
2. Run dashboard integration tests to verify the dashboard can connect to the API
3. Perform manual testing of the dashboard functionality
4. Test the proposal generation flow with test jobs
5. Verify security and performance aspects

## Rollback Procedure

In case of test failures or other issues, the following rollback procedure can be used:

```bash
# Use the existing rollback script
./rollback-test-api.sh
```

## Acceptance Criteria

The test API implementation will be considered successful if:

1. All automated tests pass successfully
2. Manual testing confirms the dashboard functionality
3. The API can serve proposal data with proper headers
4. The dashboard can display and interact with proposals
5. No security vulnerabilities are detected

## Post-Test Actions

After successful testing, the following actions should be taken:

1. Document any issues or observations
2. Update the test API setup documentation if needed
3. Prepare for production implementation
4. Ensure all test files and logs are properly backed up

## Conclusion

This test plan provides a structured approach to testing the Upwork Automation API system in the test environment. By following this plan, we can ensure that the API functions correctly and integrates properly with the dashboard before moving to production implementation. 