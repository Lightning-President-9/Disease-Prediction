let selected = new Set();
let filtered = [];
let activeIndex = -1;

const symptomInput = document.getElementById("symptomInput");
const suggestions = document.getElementById("suggestions");
const tags = document.getElementById("tags");

const emptyReport = document.getElementById("emptyReport");
const reportContent = document.getElementById("reportContent");

function filterSymptoms() {

	const query = symptomInput.value
		.toLowerCase()
		.trim();

	suggestions.innerHTML = "";

	activeIndex = -1;

	if (!query) return;


	filtered = ALL_SYMPTOMS
		.filter(symptom =>
			symptom.includes(query) &&
			!selected.has(symptom)
		)
		.slice(0, 10);


	filtered.forEach((symptom, index) => {

		const item = document.createElement("div");

		item.className = "suggestion";

		item.innerText =
			symptom.replaceAll("_", " ");

		item.onclick = () =>
			selectSymptom(index);


		suggestions.appendChild(item);
	});
}

function handleKeys(event) {

	const items =
		document.querySelectorAll(".suggestion");


	if (
		event.key === "ArrowDown" &&
		activeIndex < items.length - 1
	) {

		activeIndex++;
	} else if (
		event.key === "ArrowUp" &&
		activeIndex > 0
	) {

		activeIndex--;
	} else if (
		event.key === "Enter" &&
		activeIndex >= 0
	) {

		event.preventDefault();

		selectSymptom(activeIndex);

		return;
	}

	items.forEach((item, index) => {

		item.classList.toggle(
			"active",
			index === activeIndex
		);

	});

}

function selectSymptom(index) {

	selected.add(filtered[index]);

	symptomInput.value = "";

	suggestions.innerHTML = "";

	renderTags();

}

function renderTags() {

	tags.innerHTML = "";


	selected.forEach(symptom => {

		const tag =
			document.createElement("div");

		tag.className = "tag";

		tag.innerHTML =
			`✓ ${symptom.replaceAll("_", " ")}
             <span onclick="removeSymptom('${symptom}')">
             ×
             </span>`;

		tags.appendChild(tag);

	});

}

function removeSymptom(symptom) {

	selected.delete(symptom);

	renderTags();

}

function clearSymptoms() {

	selected.clear();

	renderTags();

	symptomInput.value = "";

	suggestions.innerHTML = "";

}

function runPrediction() {

	if (!selected.size) {

		alert(
			"Please select at least one symptom."
		);

		return;

	}

	createReportMetadata();

	const query = [...selected]
		.map(
			symptom =>
			`symptoms=${encodeURIComponent(symptom)}`
		)
		.join("&");

	fetch(`/predict?${query}`)
		.then(async response => {

			if (response.status === 429) {

				throw new Error(
					"API_LIMIT_EXCEEDED"
				);

			}

			if (!response.ok) {

				const errorData = await response.json();

				throw new Error(
					errorData.error || "Unable to process request."
				);

			}

			return response.json();

		})
		.then(data => {

			emptyReport.classList.add("hidden");

			reportContent.classList.remove("hidden");

			renderSymptomSummary();

			renderPrimaryDiagnosis(
				data.table[0]
			);

			renderTable(data.table);

			Plotly.newPlot(
				"confidenceChart",
				JSON.parse(data.confidence_chart), {
					responsive: true
				}
			);

			renderDetails(data.details);

		})
		.catch(error => {

			console.error(error);

			if (error.message === "API_LIMIT_EXCEEDED") {

				alert(
					"⚠ Too many diagnosis requests.\n\n" +
					"You have reached the usage limit for this period.\n" +
					"Please wait and try again later."
				);

			} else {

				alert(
					"⚠ Unable to generate medical report.\n\n" +
					error.message
				);

			}

		});

}

function createReportMetadata() {

	const reportId =
		"HD-" +
		new Date()
		.getTime();

	document
		.getElementById("reportId")
		.innerText = reportId;

	document
		.getElementById("reportDate")
		.innerText =
		new Date()
		.toLocaleString();

}

function renderSymptomSummary() {

	const container =
		document.getElementById("symptomSummary");

	let html = "<ul>";

	selected.forEach(symptom => {

		html += `
            <li>
                ✓ ${symptom.replaceAll("_", " ")}
            </li>
        `;

	});

	html += `
        </ul>
        <br>
        <strong>
        Total Symptoms:
        ${selected.size}
        </strong>
    `;

	container.innerHTML = html;

}

function renderPrimaryDiagnosis(result) {

	document
		.getElementById("primaryDiagnosis")
		.innerHTML = `

        <div class="primary-result">

            <p>
            Primary Diagnosis
            </p>

            <div class="disease-name">
                ${result.Disease}
            </div>

            <p>
                AI Confidence:
                ${result.Confidence}
            </p>

        </div>

    `;

}

function renderTable(rows) {

	let html = `
        <table class="data-table">

        <tr>
            <th>Rank</th>
            <th>Possible Condition</th>
            <th>Confidence</th>
        </tr>
    `;

	rows.forEach((row, index) => {


		html += `
            <tr>

            <td>
                ${index + 1}
            </td>

            <td>
                ${row.Disease}
            </td>

            <td>
                ${row.Confidence}
            </td>

            </tr>
        `;

	});

	html += "</table>";

	document
		.getElementById("table")
		.innerHTML = html;
}

function renderDetails(data) {

	const container =
		document.getElementById("medicalDetails");

	if (!data) {

		container.innerHTML =
			"<p>No medical information available.</p>";

		return;

	}

	let html = `

        <h3>
            ${data.title}
        </h3>

    `;

	const sections = [
		"Overview",
		"Symptoms",
		"Causes",
		"Risk factors",
		"Complications",
		"Prevention",
		"Diagnosis",
		"Treatment",
		"Lifestyle and home remedies"
	];

	sections.forEach(section => {

		const content =
			data.sections?.[section];

		if (content) {

			html += `
    <details class="medical-section" open>

        <summary>
            ${section}
        </summary>

        <p>
            ${content}
        </p>

    </details>
`;

		}

	});

	container.innerHTML = html;

}

document
	.getElementById("printReport")
	.addEventListener("click", function() {

		window.print();

	});

window.addEventListener(
	"load",
	function() {

		//        console.log(
		//            "HealthAI Clinical Report Ready"
		//        );

	}
);