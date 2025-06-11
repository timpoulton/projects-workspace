// Direct Data Check - Paste this in the browser console to bypass any filtering
async function forceLoadAllProposals() {
  console.clear();
  console.log('🔍 DIRECT DATA CHECK: Bypassing all filters and dashboard code');
  
  // Get timestamp for cache busting
  const timestamp = new Date().getTime();
  
  try {
    // Try multiple URLs
    const urls = [
      `https://projekt-ai.net/data/proposals.json?v=${timestamp}&_=${Math.random()}`,
      `https://projekt-ai.net/data/proposals-1748923595.json?v=${timestamp}&_=${Math.random()}`,
      `/data/proposals.json?v=${timestamp}&_=${Math.random()}`
    ];
    
    let successData = null;
    
    // Try each URL until one works
    for (const url of urls) {
      try {
        console.log(`🔄 Trying: ${url}`);
        const response = await fetch(url, {
          cache: 'no-store',
          headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
          }
        });
        
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        
        const data = await response.json();
        console.log(`✅ Success! URL: ${url}`);
        successData = data;
        break;
      } catch (err) {
        console.warn(`⚠️ Failed with ${url}: ${err.message}`);
      }
    }
    
    if (!successData) {
      throw new Error('All URLs failed');
    }
    
    // Show detailed information about the data
    console.log('📊 DATA LOADED:', {
      totalCountInJson: successData.total_count,
      actualProposalsLength: successData.proposals ? successData.proposals.length : 0,
      generatedAt: successData.generated_at
    });
    
    if (successData.proposals && successData.proposals.length > 0) {
      console.log('📋 PROPOSAL IDs (first 5):');
      successData.proposals.slice(0, 5).forEach((p, i) => {
        console.log(`${i+1}. ${p.job_id || 'unknown'}: ${p.job_title || 'untitled'}`);
      });
      
      // Display the proposals on the page
      const container = document.getElementById('proposalsContainer');
      if (container) {
        // Add header with counts
        container.innerHTML = `
          <div style="background: #1a1a1a; padding: 20px; margin-bottom: 20px; border-radius: 8px;">
            <h2>DIRECT DATA CHECK RESULTS</h2>
            <p>JSON total_count: ${successData.total_count}</p>
            <p>Actual proposals: ${successData.proposals.length}</p>
            <p>Last updated: ${new Date(successData.generated_at).toLocaleString()}</p>
          </div>
        `;
        
        // Add each proposal
        successData.proposals.forEach((proposal, index) => {
          container.innerHTML += `
            <div style="background: rgba(255,255,255,0.05); padding: 20px; margin-bottom: 10px; border-radius: 8px;">
              <h3>${index + 1}. ${proposal.job_title || 'No Title'}</h3>
              <p><strong>ID:</strong> ${proposal.job_id}</p>
              <p><strong>Client:</strong> ${proposal.client_name || 'Unknown'}</p>
              <p><strong>Score:</strong> ${proposal.score || 0}</p>
            </div>
          `;
        });
      } else {
        console.error('❌ Could not find proposalsContainer element');
      }
    } else {
      console.warn('⚠️ No proposals found in the data');
    }
    
  } catch (error) {
    console.error('❌ ERROR:', error);
  }
}

// Execute the function
forceLoadAllProposals(); 