function submitRepo() {
  const repoUrl = document.getElementById("repoUrl").value.trim();
  const output = document.getElementById("output");

  if (!repoUrl) {
    output.textContent = "Please enter a repository URL.";
    return;
  }

  output.textContent = "Running Dead Link Fixer...";

  fetch("http://localhost:5000/fix-dead-links", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ repo_url: repoUrl })
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        output.textContent = "Error: " + data.error;
      } else {
        let html = `<strong>${data.message}</strong><br>`;
        if (data.pull_request_url) {
          html += `<a href="${data.pull_request_url}" target="_blank">View Pull Request</a><br>`;
        }
        if (data.modified_files && data.modified_files.length > 0) {
          html += `<br><strong>Modified files:</strong><br><pre>${data.modified_files.join('\n')}</pre>`;
        } else if (!data.pull_request_url) {
          html += `<br>No pull request created.`;
        }
        output.innerHTML = html;
      }
    })
    .catch(err => {
      output.textContent = "Unexpected error: " + err;
    });
}
