# Webflow Integration Guide for Club77 Guest List

This guide explains how to set up your Webflow form to send data directly to the Club77 Guest List application.

## Webflow Form Configuration

1. **Log in to your Webflow account** and navigate to your site's dashboard.

2. **Open the Designer** for your site.

3. **Select the guest list form** you want to integrate.

4. **Go to Form Settings**:
   - Click on the form element
   - In the right panel, click on "Form Settings"

5. **Set the Form Integration**:
   - Select "Custom" as the integration type
   - Set the Form Action to the webhook URL: `http://guestlist.club77.com.au:8080/api/webhooks/guest-list-registration`
   - Method: POST

6. **Set the webhook header**:
   - In the "Custom Headers" section, add:
   - Name: `x-webflow-webhook-secret`
   - Value: `7ba02129304569b5b6edbc622b1600371e9cb9e46bd5f760f701450d4aa09899`

7. **Map form fields**:
   Ensure your form fields use these exact names to match our database:
   - `first_name`: The guest's first name
   - `last_name`: The guest's last name
   - `email`: The guest's email address
   - `dob`: Date of birth (YYYY-MM-DD format)
   - `event_name`: Name of the event
   - `event_date`: Date of the event (YYYY-MM-DD format)

8. **Publish your site** to apply the changes.

## Testing the Integration

1. Submit a test entry through your Webflow form.

2. Check the Club77 Guest List application to verify the data was received:
   - Go to: `http://guestlist.club77.com.au:8080`
   - Navigate to the Events page
   - Select the event you submitted
   - Verify the guest appears in the list

## Troubleshooting

If the form submission isn't showing up in the guest list:

1. **Check the form field names** in Webflow to ensure they match exactly (`first_name`, `last_name`, etc.)

2. **Verify the webhook URL** is correct (including port number 8080)

3. **Check the server logs** for any errors:
   ```
   cd ~/homelab-docs/club77-checkin && docker-compose logs app
   ```

4. **Test the webhook endpoint** directly:
   ```
   curl -X POST -H "Content-Type: application/json" \
   -H "x-webflow-webhook-secret: 7ba02129304569b5b6edbc622b1600371e9cb9e46bd5f760f701450d4aa09899" \
   -d '{"event_name":"Test Event","first_name":"John","last_name":"Doe","email":"test@example.com","dob":"1990-01-01"}' \
   http://localhost:3001/api/webhooks/guest-list-registration
   ```

## Need Help?

Contact your developer for assistance with this integration. 