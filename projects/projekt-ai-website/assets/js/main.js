(()=>{document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll('a[href^="#"]').forEach(t=>{t.addEventListener("click",function(e){e.preventDefault();let o=this.getAttribute("href"),n=document.querySelector(o);n&&window.scrollTo({top:n.offsetTop-80,behavior:"smooth"})})});let c=document.querySelectorAll("section"),v=document.querySelectorAll(".nav-links a");window.addEventListener("scroll",()=>{let t="";c.forEach(e=>{let o=e.offsetTop,n=e.clientHeight;scrollY>=o-100&&(t=e.getAttribute("id"))}),v.forEach(e=>{e.classList.remove("active"),e.getAttribute("href").substring(1)===t&&e.classList.add("active")}),c.forEach(e=>{let o=e.offsetTop;scrollY>=o-window.innerHeight/1.2&&e.classList.add("animated")})}),document.querySelectorAll(".btn, .demo-button, .workflow-button").forEach(t=>{t.addEventListener("mouseenter",()=>{t.style.transform="translateY(-3px)"}),t.addEventListener("mouseleave",()=>{t.style.transform="translateY(0)"})});let w=document.querySelectorAll(".gradient-text"),i=0;function d(){i=(i+.5)%360,w.forEach(t=>{t.style.background=`linear-gradient(${i}deg, #00c6ff, #bc61ff)`,t.style.webkitBackgroundClip="text",t.style.backgroundClip="text",t.style.color="transparent"}),requestAnimationFrame(d)}d();let l=document.querySelectorAll(".tab-button"),u=document.querySelectorAll(".demo-panel");l.length>0&&u.length>0&&l.forEach(t=>{t.addEventListener("click",()=>{l.forEach(n=>n.classList.remove("active")),u.forEach(n=>n.classList.remove("active")),t.classList.add("active");let e=t.getAttribute("data-tab"),o=document.getElementById(e);o&&(o.classList.add("active"),o.style.opacity=0,o.style.transform="translateY(20px)",setTimeout(()=>{o.style.transition="opacity 0.5s, transform 0.5s",o.style.opacity=1,o.style.transform="translateY(0)"},50))})});let a=document.getElementById("contactForm");a&&a.addEventListener("submit",function(t){t.preventDefault();let e=document.getElementById("name").value,o=document.getElementById("email").value,n=document.getElementById("message").value;alert(`Thank you for your message, ${e}! We'll get back to you at ${o} soon.`),a.reset()});let s=document.querySelector(".workflow-modal"),p=document.querySelector(".close-modal"),m={"customer-support":{title:"Customer Support Automation Workflow",image:"assets/img/workflow-support.png",description:`
                <p>This automation workflow reduces response times by 68% through intelligent ticket routing and AI-powered response generation.</p>
                <h4>Key Components:</h4>
                <ul>
                    <li><strong>Intelligent Ticket Classification:</strong> Automatically categorizes incoming support requests based on content analysis</li>
                    <li><strong>Priority Assignment:</strong> Uses predefined rules to assign priority levels based on customer tier, issue type, and keywords</li>
                    <li><strong>Agent Matching:</strong> Routes tickets to the most appropriate agent based on expertise, availability, and historical performance</li>
                    <li><strong>AI Response Generation:</strong> Provides agents with response templates and suggestions based on similar past tickets</li>
                    <li><strong>Automated Follow-up:</strong> Schedules follow-up communications and satisfaction surveys</li>
                </ul>
                <p>This workflow can be customized for your specific support channels, team structure, and business rules.</p>
            `},"data-processing":{title:"Data Processing Pipeline",image:"assets/img/workflow-data.png",description:`
                <p>This end-to-end data automation workflow saves 15+ hours weekly by streamlining data collection, cleaning, analysis, and reporting.</p>
                <h4>Key Components:</h4>
                <ul>
                    <li><strong>Data Collection:</strong> Automated gathering from multiple sources (APIs, databases, files) on schedule or trigger</li>
                    <li><strong>Data Validation:</strong> Checks for missing values, duplicates, and format inconsistencies</li>
                    <li><strong>Data Transformation:</strong> Applies specified business rules and conversions</li>
                    <li><strong>Analysis Engine:</strong> Processes data through predefined models and algorithms</li>
                    <li><strong>Reporting:</strong> Generates dashboards and distributes reports to stakeholders</li>
                    <li><strong>Error Handling:</strong> Detects and resolves common issues without manual intervention</li>
                </ul>
                <p>This workflow can be adapted to your data sources, analysis requirements, and reporting needs.</p>
            `},"sales-leads":{title:"Sales Lead Qualification System",image:"assets/img/workflow-sales.png",description:`
                <p>This AI-powered lead qualification workflow increased conversion rates by 32% by automating the scoring and routing of sales leads.</p>
                <h4>Key Components:</h4>
                <ul>
                    <li><strong>Lead Capture:</strong> Collects prospect information from website forms, social media, and other channels</li>
                    <li><strong>Enrichment:</strong> Augments lead data with information from third-party sources</li>
                    <li><strong>Scoring Algorithm:</strong> Assigns quality scores based on demographic, behavioral, and engagement factors</li>
                    <li><strong>Segmentation:</strong> Categorizes leads by buyer persona, industry, and purchase intent</li>
                    <li><strong>Sales Rep Assignment:</strong> Routes qualified leads to appropriate sales team members</li>
                    <li><strong>Follow-up Automation:</strong> Schedules personalized outreach through preferred channels</li>
                </ul>
                <p>This workflow can be tailored to your specific sales process, qualification criteria, and CRM system.</p>
            `}};document.querySelectorAll(".workflow-button").forEach((t,e)=>{t.addEventListener("click",function(){let o,n=this.closest(".workflow-card").querySelector("h3").textContent.toLowerCase();if(n.includes("customer support")?o="customer-support":n.includes("data processing")?o="data-processing":n.includes("sales lead")&&(o="sales-leads"),o&&m[o]){let r=m[o];s.querySelector(".modal-title").textContent=r.title,s.querySelector(".modal-image").src=r.image,s.querySelector(".modal-description").innerHTML=r.description,s.style.display="flex",s.style.opacity=0,document.body.style.overflow="hidden",setTimeout(()=>{s.style.transition="opacity 0.3s ease",s.style.opacity=1},50)}})}),p&&p.addEventListener("click",function(){s.style.opacity=0,setTimeout(()=>{s.style.display="none",document.body.style.overflow="auto"},300)}),s&&s.addEventListener("click",function(t){t.target===s&&(s.style.opacity=0,setTimeout(()=>{s.style.display="none",document.body.style.overflow="auto"},300))}),document.querySelectorAll(".demo-button").forEach(t=>{t.addEventListener("click",function(){let e=this.closest(".demo-panel");if(e){let o=e.querySelector("h3").textContent,n=document.createElement("div");n.className="demo-popup",n.innerHTML=`
                    <div class="demo-popup-content">
                        <button class="close-popup">&times;</button>
                        <h3>Demo Coming Soon</h3>
                        <p>${o} demo is currently in development.</p>
                        <p>Sign up for early access to our platform demos.</p>
                        <div class="popup-actions">
                            <button class="btn btn-primary popup-signup">Sign Up for Early Access</button>
                        </div>
                    </div>
                `,document.body.appendChild(n),document.body.style.overflow="hidden",setTimeout(()=>{n.style.opacity=1},50),n.querySelector(".close-popup").addEventListener("click",()=>{n.style.opacity=0,setTimeout(()=>{document.body.removeChild(n),document.body.style.overflow="auto"},300)}),n.querySelector(".popup-signup").addEventListener("click",()=>{n.style.opacity=0,setTimeout(()=>{document.body.removeChild(n),document.body.style.overflow="auto";let r=document.querySelector("#contact");r&&window.scrollTo({top:r.offsetTop-80,behavior:"smooth"})},300)})}})});let y=document.querySelector(".workflow-request .btn");y&&y.addEventListener("click",function(){let t=document.querySelector("#contact");t&&window.scrollTo({top:t.offsetTop-80,behavior:"smooth"})});let g=document.querySelector(".request-customization"),f=document.querySelector(".download-workflow");g&&g.addEventListener("click",function(){s.style.opacity=0,setTimeout(()=>{s.style.display="none",document.body.style.overflow="auto";let t=document.querySelector("#contact");t&&window.scrollTo({top:t.offsetTop-80,behavior:"smooth"})},300)}),f&&f.addEventListener("click",function(){let t=s.querySelector(".modal-image").src,e=s.querySelector(".modal-title").textContent,o=document.createElement("a");o.href=t,o.download=e.replace(/\s+/g,"-").toLowerCase()+".png",o.click()});let h=document.querySelector(".signup-offer .btn");h&&h.addEventListener("click",function(t){t.preventDefault();let e=document.createElement("div");e.className="demo-popup",e.innerHTML=`
                <div class="demo-popup-content">
                    <button class="close-popup">&times;</button>
                    <h3>Get Your Free Credits</h3>
                    <p>Sign up now to receive $200 in free credits to try our platform.</p>
                    <form id="signupForm" class="popup-form">
                        <div class="form-group">
                            <label for="signup-name" class="form-label">Your Name</label>
                            <input type="text" id="signup-name" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="signup-email" class="form-label">Your Email</label>
                            <input type="email" id="signup-email" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="signup-company" class="form-label">Company Name</label>
                            <input type="text" id="signup-company" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Sign Up</button>
                    </form>
                </div>
            `,document.body.appendChild(e),document.body.style.overflow="hidden",setTimeout(()=>{e.style.opacity=1},50),e.querySelector(".close-popup").addEventListener("click",()=>{e.style.opacity=0,setTimeout(()=>{document.body.removeChild(e),document.body.style.overflow="auto"},300)}),e.querySelector("#signupForm").addEventListener("submit",o=>{o.preventDefault();let n=e.querySelector("#signup-name").value,r=e.querySelector("#signup-email").value;e.querySelector(".demo-popup-content").innerHTML=`
                    <h3>Thank You!</h3>
                    <p>Thanks, ${n}! We've sent your free credits information to ${r}.</p>
                    <p>You can start using the platform immediately.</p>
                    <button class="btn btn-primary close-popup">Close</button>
                `,e.querySelector(".close-popup").addEventListener("click",()=>{e.style.opacity=0,setTimeout(()=>{document.body.removeChild(e),document.body.style.overflow="auto"},300)})})});let b=document.createElement("style");b.textContent=`
        .demo-popup {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(6, 12, 36, 0.9);
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .demo-popup-content {
            background-color: var(--bg-secondary);
            padding: 2.5rem;
            border-radius: var(--border-radius);
            max-width: 500px;
            width: 90%;
            position: relative;
            border: 1px solid var(--border-color);
        }
        
        .close-popup {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 28px;
            color: var(--text-secondary);
            cursor: pointer;
            background: none;
            border: none;
            transition: var(--transition);
        }
        
        .close-popup:hover {
            color: var(--accent-color);
        }
        
        .popup-form {
            margin-top: 1.5rem;
        }
        
        .popup-actions {
            margin-top: 1.5rem;
            display: flex;
            justify-content: center;
        }
    `,document.head.appendChild(b)});})();
