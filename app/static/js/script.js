// Function to load Ivy League Opportunities
async function loadOpportunities() {
  // Check both potential IDs to be safe
  const grid =
    document.getElementById("opportunity-feed") ||
    document.getElementById("content-grid");
  if (!grid) {
    console.error("Could not find a container to put the data in!");
    return;
  }

  grid.innerHTML = "<p class='loading'>Scanning Ivy League platforms...</p>";

  try {
    const response = await fetch("/opportunities");
    const data = await response.json();

    if (data.length === 0) {
      grid.innerHTML =
        "<div class='empty'>No data yet. Click 'Sync Intelligence'.</div>";
      return;
    }

    grid.innerHTML = data
      .map(
        (opp) => `
            <div class="card">
                <div class="card-header">
                    <span class="tag">${opp.domain || "General"}</span>
                    <span class="univ-badge">${opp.university}</span>
                </div>
                <h3>${opp.title}</h3>
                <p>${opp.description}</p>
                <div class="card-footer">
                    <a href="${opp.link}" target="_blank" class="apply-link">View Details →</a>
                    <button onclick="generateQuickApply('${opp.title}', '${opp.university}')" class="btn-mini">Quick Apply</button>
                </div>
            </div>
        `,
      )
      .join("");
  } catch (e) {
    grid.innerHTML = "<p>Server Connection Error.</p>";
  }
}

// Fixed Sync Trigger for the Floating Button
async function triggerScrape() {
  console.log("Sync started...");

  // Safety check for the button
  const btn = document.querySelector(".floating-sync");
  const originalText = btn ? btn.innerHTML : "Sync Intelligence";

  if (btn) {
    btn.innerHTML = "<span>⏳</span> Syncing...";
    btn.disabled = true;
  }

  try {
    const response = await fetch("/scrape-now");
    const result = await response.json();

    console.log("Server response:", result);
    alert(`Aggregator Updated: ${result.new_added} new items found.`);

    // Refresh the feed
    loadOpportunities();
  } catch (error) {
    console.error("Sync Error:", error);
    alert("Intelligence Sync Failed. Check if the server is running.");
  } finally {
    if (btn) {
      btn.innerHTML = originalText;
      btn.disabled = false;
    }
  }
}

async function recordApplication(oppId) {
  // This calls a new backend route we'll build to save the application
  const response = await fetch(`/apply/${oppId}?user_id=1`, { method: "POST" });
  if (response.ok) {
    alert("Application tracked in your history!");
  }
}

async function recordApplication(oppId) {
  // This calls a new backend route we'll build to save the application
  const response = await fetch(`/apply/${oppId}?user_id=1`, { method: "POST" });
  if (response.ok) {
    alert("Application tracked in your history!");
  }
}

// NEW: Function to load the InCoScore Leaderboard
async function loadLeaderboard() {
  const grid = document.getElementById("content-grid");
  document.getElementById("page-title").innerText = "InCoScore Leaderboard";
  grid.innerHTML = "<p>Ranking students...</p>";

  try {
    const response = await fetch("/community/leaderboard");
    const data = await response.json();

    if (data.length === 0) {
      grid.innerHTML =
        "<p>The leaderboard is currently empty. Start building your profile!</p>";
      return;
    }

    // Create a table for a professional academic look
    grid.innerHTML = `
            <div class="leaderboard-container" style="width: 100%; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead style="border-bottom: 2px solid #eee;">
                        <tr>
                            <th style="padding: 10px;">Rank</th>
                            <th style="padding: 10px;">Student Name</th>
                            <th style="padding: 10px;">InCoScore</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data
                          .map(
                            (user, index) => `
                            <tr style="border-bottom: 1px solid #fafafa;">
                                <td style="padding: 10px;">#${index + 1}</td>
                                <td style="padding: 10px;"><strong>${user.full_name}</strong></td>
                                <td style="padding: 10px; color: #00356b; font-weight: bold;">${user.incoscore.toFixed(2)}</td>
                            </tr>
                        `,
                          )
                          .join("")}
                    </tbody>
                </table>
            </div>
        `;
  } catch (error) {
    grid.innerHTML = "<p>Error fetching leaderboard data.</p>";
  }
}

async function triggerScrape() {
  // 1. Identify the new sidebar button
  const btn = document.getElementById("sidebar-sync-btn");
  const originalContent = btn.innerHTML;

  // 2. Visual Feedback
  btn.innerHTML = "<span>⏳</span> Monitoring Ivy Sites...";
  btn.style.opacity = "0.7";
  btn.disabled = true;

  console.log("Starting Ivy League Intelligence Scrape...");

  try {
    // 3. Call the FastAPI backend
    const response = await fetch("/scrape-now");

    if (!response.ok) throw new Error("Server response was not OK");

    const result = await response.json();

    // 4. Update the user on results
    console.log("Scrape successful:", result);
    alert(
      `Aggregator Updated!\nTotal Scraped: ${result.scraped}\nNew Items Added: ${result.new_added}`,
    );

    // 5. Force refresh the feed
    loadOpportunities();
  } catch (error) {
    console.error("Scrape Error:", error);
    alert(
      "Could not connect to Ivy League sites. Check your internet or server.",
    );
  } finally {
    // 6. Restore button state
    btn.innerHTML = originalContent;
    btn.style.opacity = "1";
    btn.disabled = false;
  }
}

// Automatically load data when page opens
window.onload = loadOpportunities;
// Function to show the profile update form
function showProfileUpdate() {
  document.getElementById("page-title").innerText =
    "Personal Competency Network";
  document.getElementById("content-grid").style.display = "none";
  document.getElementById("profile-section").style.display = "block";
}

// Function to send data to FastAPI
async function submitProfileUpdate() {
  // For now, we use user_id = 1 (your first test user)
  const userId = 1;
  const research = document.getElementById("research-count").value;
  const hackathons = document.getElementById("hackathon-count").value;
  const internships = 0; // Internships can be added to the API next

  try {
    // Calling the endpoint we created in auth.py
    const response = await fetch(
      `/user/update-profile/${userId}?research=${research}&hackathons=${hackathons}`,
      {
        method: "PUT",
      },
    );

    const result = await response.json();

    if (response.ok) {
      alert(`Profile Updated! Your new InCoScore is: ${result.new_incoscore}`);
      location.reload(); // Refresh to see changes on leaderboard
    } else {
      alert("Error: " + result.detail);
    }
  } catch (error) {
    alert("Failed to update profile. Ensure your API is running.");
  }
}
async function checkNotifications(interest = "Artificial Intelligence") {
  const response = await fetch(`/notifications/${interest}`);
  const matches = await response.json();

  if (matches.length > 0) {
    // Find the cards on the screen and highlight the matching ones
    const cards = document.querySelectorAll(".card");
    cards.forEach((card) => {
      if (card.innerHTML.includes(interest)) {
        card.style.border = "2px solid #27ae60"; // Green highlight
        card.style.background = "#f0fff4";
        const badge = document.createElement("div");
        badge.innerText = "✨ Recommended for You";
        badge.style =
          "font-size: 10px; color: #27ae60; font-weight: bold; margin-bottom: 5px;";
        card.prepend(badge);
      }
    });
  }
}
async function generateQuickApply(oppTitle, univ) {
  // 1. Fetch current student stats (Research, Hackathons)
  const response = await fetch(
    "/user/update-profile/1?research=0&hackathons=0",
  );
  const user = await response.json();

  // 2. Create the AI-augmented application draft
  const draft = `Subject: Interest in ${oppTitle} at ${univ}
    
Dear ${univ} Admissions,

My name is [Your Name], and I am a high-competency student with an InCoScore of ${user.new_incoscore.toFixed(1)}. 
I have successfully completed ${document.getElementById("research-count").value} research papers and 
participated in ${document.getElementById("hackathon-count").value} hackathons. 

I believe my profile is a strong match for this opportunity. 
Reference ID: ${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

  // 3. Copy to clipboard
  await navigator.clipboard.writeText(draft);
  alert(
    `Draft generated for ${univ}!\n\nYour InCoScore (${user.new_incoscore.toFixed(1)}) has been included to boost your profile.`,
  );
}
async function runIntelligenceSync() {
  // 1. Forced element lookup
  const btn =
    document.getElementById("sidebar-sync-btn") ||
    document.querySelector('button[onclick*="Sync"]');

  if (!btn) {
    console.warn("Sync button not found yet, retrying in 500ms...");
    setTimeout(runIntelligenceSync, 500);
    return;
  }

  btn.disabled = true;
  btn.innerHTML = "<span>⏳</span> FORCE SYNCING...";

  try {
    // 2. Trigger the Scraper
    const response = await fetch("/scrape-now");
    const result = await response.json();

    // 3. Clear existing feed to force visual update
    document.getElementById("opportunity-feed").innerHTML = "";

    alert(
      `Success! Aggregated ${result.new_added} new Ivy League opportunities.`,
    );
    loadOpportunities();
  } catch (error) {
    alert("Sync Failed: Ensure FastAPI is running on port 8000.");
  } finally {
    btn.disabled = false;
    btn.innerHTML = "<span class='icon'>🔄</span> Sync Intelligence";
  }
}
