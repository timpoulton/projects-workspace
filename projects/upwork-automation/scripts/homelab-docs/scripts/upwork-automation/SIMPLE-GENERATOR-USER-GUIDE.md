# Upwork Proposal Generator - User Guide

## 🚀 Quick Start

### 1. Start the System

```bash
cd /root/homelab-docs/scripts/upwork-automation
python3 simple-upwork-generator.py
```

### 2. Access the Dashboard

Open your browser to: **http://192.168.1.107:5056**

### 3. Configure Chrome Extension

Set your Chrome extension webhook URL to:
```
http://192.168.1.107:5056/webhook/rss-jobs
```

## 📋 How to Use

### Viewing Jobs

1. **Jobs from Chrome Extension** - All jobs scraped by your Chrome extension appear automatically
2. **Job Cards Display**:
   - Job title and budget
   - Client name
   - Score indicator (color-coded: green=high, yellow=medium, red=low)
   - Brief description preview
   - Timestamp

### Generating Proposals

1. **Find a job** you're interested in
2. **Click "Generate Proposal"** button
3. **Wait** for the AI to analyze and generate (usually 5-10 seconds)
4. **View** the beautifully formatted proposal with:
   - Custom message tailored to the job
   - Professional dark-themed layout
   - Industry analysis
   - Implementation steps
   - Why you're the perfect fit

### Managing Jobs

- **Reject Jobs**: Click the "Reject" button to remove jobs you're not interested in
- **Manual Entry**: Use the form at the bottom to add jobs by URL

## 🎯 Understanding Scores

The AI scores jobs from 0-100 based on:

- **Budget** (30 points max)
  - $5,000+: 30 points
  - $2,000-$5,000: 25 points
  - $1,000-$2,000: 20 points
  - $500-$1,000: 15 points
  - Under $500: 10 points

- **Keywords** (40 points max)
  - automation, workflow, integration: 10 points each
  - api, zapier, make, n8n: 8 points each

- **Client Quality** (20 points max)
  - Payment verified: 10 points
  - High spend history: 10 points

- **Job Clarity** (10 points max)
  - Clear requirements: 10 points

## 🔧 Troubleshooting

### Jobs Not Appearing

1. **Check Chrome Extension**:
   - Is it running?
   - Is webhook URL correct?
   - Try sending a test job

2. **Test the Webhook**:
   ```bash
   python3 test-webhook.py
   ```

3. **Check Server Logs**:
   ```bash
   tail -f simple-generator.log
   ```

### Proposals Not Generating

1. **Check Multi-Model Server**:
   ```bash
   ps aux | grep multimodel
   ```

2. **Start if Needed**:
   ```bash
   python3 upwork-proposal-server-multimodel.py &
   ```

3. **Test Full System**:
   ```bash
   python3 test-proposal-generation.py
   ```

### Can't Access Dashboard

1. **Check Server Running**:
   ```bash
   ps aux | grep simple-upwork-generator
   ```

2. **Check Port**:
   ```bash
   netstat -tlnp | grep 5056
   ```

3. **Restart if Needed**:
   ```bash
   pkill -f "simple-upwork-generator.py"
   python3 simple-upwork-generator.py
   ```

## 📊 Viewing Logs

### Application Logs
```bash
tail -f simple-generator.log
```

### Server Output
```bash
# If running in foreground, you'll see logs in terminal
# If running in background:
tail -f server.log
```

### Multi-Model AI Logs
```bash
# Check the terminal where multimodel server is running
```

## 🎨 Proposal Quality Tips

The AI generates better proposals when jobs have:

1. **Clear Requirements** - Detailed job descriptions
2. **Specific Technologies** - Mentions of tools/platforms
3. **Budget Information** - Clear budget ranges
4. **Project Scope** - Well-defined deliverables

## 🔄 Daily Workflow

1. **Morning**:
   - Start the server
   - Check for new jobs from overnight
   - Generate proposals for high-score jobs

2. **Throughout the Day**:
   - Monitor new jobs as they come in
   - Generate proposals for interesting opportunities
   - Reject jobs that don't fit

3. **End of Day**:
   - Review generated proposals
   - Copy personalized messages to Upwork
   - Submit proposals on Upwork platform

## 📝 Copying Proposals to Upwork

1. **Generate the proposal** in the system
2. **Copy the message** from the proposal page
3. **Go to Upwork** and find the job
4. **Paste the message** in the proposal form
5. **Attach your portfolio** items as needed
6. **Submit** the proposal

## 🚨 Important Notes

- The system generates proposals but does **NOT** submit them to Upwork
- Always review proposals before sending
- Customize further if needed for high-value opportunities
- Keep your Chrome extension running for continuous job collection

## 💡 Pro Tips

1. **Batch Processing**: Let jobs accumulate, then process the best ones
2. **Score Threshold**: Focus on jobs scoring 70+ for best ROI
3. **Quick Reject**: Don't hesitate to reject poor-fit jobs
4. **Template Evolution**: The AI learns from patterns - feed it good jobs

## 🆘 Getting Help

1. **Check Documentation**:
   - README.md - System overview
   - This guide - User instructions
   - Test scripts - Verify functionality

2. **Run Tests**:
   ```bash
   python3 test-proposal-generation.py
   ```

3. **Check All Services**:
   ```bash
   ./check-system-health.sh
   ```

Remember: This system is designed to save you time by automating the proposal creation process, but your expertise and personal touch in reviewing and customizing proposals is what wins clients! 