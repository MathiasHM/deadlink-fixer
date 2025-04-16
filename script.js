function submitRepo() {
    const repoUrl = document.getElementById("repoUrl").value.trim();
    const output = document.getElementById("output");

    if (!repoUrl) {
        output.textContent = "Please enter a repository URL.";
        return;
    }

    output.textContent = "Running Dead Link Fixer...";

    fetch(CONFIG.BACKEND_URL/fix-dead-links", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            repo_url: repoUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            output.textContent = "Error: " + data.error;
        } else {
            output.innerHTML = ""; // clear output

            const msg = document.createElement("strong");
            msg.textContent = data.message;
            output.appendChild(msg);

            if (data.pull_request_url) {
                const prLabel = document.createElement("div");
                prLabel.innerHTML = `🔗 Pull request: `;

                const prLink = document.createElement("a");
                prLink.href = data.pull_request_url;
                prLink.target = "_blank";
                prLink.textContent = data.pull_request_url;

                prLabel.appendChild(prLink);
                output.appendChild(document.createElement("br"));
                output.appendChild(document.createElement("br"));
                output.appendChild(prLabel);
            }

            if (data.modified_files?.length > 0) {
                const listTitle = document.createElement("div");
                listTitle.innerHTML = `📝 Modified files:`;
                output.appendChild(document.createElement("br"));
                output.appendChild(listTitle);

                const list = document.createElement("ul");
                data.modified_files.forEach(file => {
                    const li = document.createElement("li");
                    li.textContent = file;
                    list.appendChild(li);
                });
                output.appendChild(list);
            }

        }
    })
    .catch(err => {
        output.textContent = "Unexpected error: " + err;
    });
}

function loginWithGithub() {
  if (typeof CONFIG === 'undefined' || !CONFIG.BACKEND_URL) {
    alert("Backend URL not configured.");
    return;
  }
  window.location.href = CONFIG.BACKEND_URL + "/login";
}