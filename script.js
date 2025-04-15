function submitRepo() {
  const repoUrl = document.getElementById("repoUrl").value.trim();
  const output = document.getElementById("output");

  if (!repoUrl) {
    output.textContent = "Please enter a repository URL.";
    return;
  }

  output.textContent = "Running Dead Link Fixer...";

  fetch("https://deadlink-fixer.onrender.com/fix-dead-links", {
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
        let result = `<strong>${data.message}</strong>`;
		if (data.pull_request_url) {
			result += `<br><br>🔗 Pull request: <a href="${data.pull_request_url}" target="_blank">${data.pull_request_url}</a>`;
		}
		if (data.modified_files?.length > 0) {
			result += `<br><br>📝 Modified files:<ul>`;
			data.modified_files.forEach(file => {
			result += `<li>${file}</li>`;
		});
		result += `</ul>`;
		}
		output.innerHTML = result;
      }
    })
    .catch(err => {
      output.textContent = "Unexpected error: " + err;
    });
}
