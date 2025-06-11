# User Guide

This guide will help you use the Upwork Scraper & Proposal Generator effectively.

## Getting Started

After [installing the system](INSTALLATION.md), you can access the web interface at http://localhost:5055 (or the configured port).

## Main Features

### 1. Searching for Jobs

The home page provides a search interface where you can:

- Enter search keywords related to your skills
- Select job categories (optional)
- Set budget range (optional)
- Choose posting date range (optional)

Click "Search Jobs" to start the scraping process. The system will:
1. Log into Upwork using your credentials
2. Navigate to the search results page
3. Extract job details and display them in a list

### 2. Managing Job Results

After searching, you'll see a list of jobs with the following information:
- Job title
- Client name
- Budget
- Job description (truncated)
- Match score (calculated based on your skills and the job requirements)

For each job, you can:
- Click "View Details" to see the full job description
- Click "Generate Proposal" to create a proposal for this job
- Click "Reject" to remove the job from your list

### 3. Generating Proposals

When you click "Generate Proposal", the system will:
1. Send the job details to the Multi-Model AI server
2. Process the job information to create a customized proposal
3. Display the formatted proposal with the professional dark theme

The proposal includes:
- Client name and job title
- Analysis of client needs
- Customized pitch based on job requirements
- Your experience relevant to the job
- Implementation plan
- Budget and timeline

### 4. Managing Generated Proposals

After a proposal is generated, you can:
- Copy the proposal text to paste into Upwork
- Download the proposal as HTML or PDF
- Edit the proposal if needed
- Return to the job list to work on other proposals

## Workflow Example

Here's a typical workflow:

1. Start with a search for "Python automation" jobs
2. Review the list of 15 jobs that appear
3. Reject 10 that don't match your skills or have low budgets
4. Generate proposals for the 5 remaining jobs
5. Submit these proposals on Upwork

## Tips for Best Results

- **Use Specific Search Terms**: More specific searches yield better results
- **Check the Score**: Jobs with higher match scores are better candidates
- **Review Before Generating**: Always read the full job description before generating a proposal
- **Customize Generated Proposals**: Add personal touches to the AI-generated proposals
- **Use Multiple Chrome Versions**: If you encounter scraping issues, try adding different Chrome versions in the config

## Troubleshooting

- **"No Jobs Found"**: Try different search terms or check your Upwork login
- **Slow Scraping**: This is normal, as the system navigates carefully to avoid being blocked
- **Proposal Generation Fails**: Check that the Multi-Model AI server is running

## Next Steps

For information on customizing the system or contributing to development, see the [Development Guide](DEVELOPMENT.md). 