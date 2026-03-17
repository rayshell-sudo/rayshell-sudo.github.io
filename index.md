---
layout: default
title: Home
---

# Hello 👋

This is my GitHub Pages site powered by Jekyll.

## Number Randomiser

<section id="number-randomiser" aria-label="Number randomiser">
	<form id="randomiser-form" novalidate>
		<div class="field-row">
			<label for="min-value">Minimum</label>
			<input id="min-value" name="min" type="number" inputmode="numeric" value="1" required>
		</div>
		<div class="field-row">
			<label for="max-value">Maximum</label>
			<input id="max-value" name="max" type="number" inputmode="numeric" value="100" required>
		</div>
		<button type="submit" id="generate-btn">Generate Number</button>
		<p id="randomiser-error" role="status" aria-live="polite"></p>
	</form>

	<div class="result-panel" aria-live="polite">
		<p class="result-label">Current Result</p>
		<p id="result-value">-</p>
	</div>

	<div class="history-panel">
		<h3>Last 10 Numbers</h3>
		<ul id="history-list" aria-live="polite"></ul>
	</div>
</section>

<style>
	#number-randomiser {
		margin-top: 1.5rem;
		padding: 1.25rem;
		border: 1px solid #d7e2eb;
		border-radius: 10px;
		background: #f8fbfe;
	}

	#randomiser-form {
		display: grid;
		grid-template-columns: repeat(2, minmax(120px, 1fr));
		gap: 0.75rem;
		align-items: end;
	}

	#number-randomiser .field-row {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}

	#number-randomiser label {
		font-size: 0.95rem;
		font-weight: 600;
	}

	#number-randomiser input {
		border: 1px solid #c3cfda;
		border-radius: 6px;
		padding: 0.5rem 0.65rem;
		font-size: 1rem;
	}

	#generate-btn {
		grid-column: 1 / -1;
		justify-self: start;
		padding: 0.55rem 0.9rem;
		border: 0;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 600;
	}

	#randomiser-error {
		grid-column: 1 / -1;
		min-height: 1.2rem;
		margin: 0;
		color: #b21f2d;
		font-size: 0.9rem;
	}

	#number-randomiser .result-panel {
		margin-top: 1rem;
		padding: 0.8rem;
		border-radius: 8px;
		background: #ffffff;
		border: 1px solid #d7e2eb;
	}

	#number-randomiser .result-label {
		margin: 0;
		font-size: 0.9rem;
		color: #4f6479;
	}

	#result-value {
		margin: 0.15rem 0 0;
		font-size: 2rem;
		font-weight: 700;
		line-height: 1.2;
	}

	#number-randomiser .history-panel {
		margin-top: 1rem;
	}

	#number-randomiser .history-panel h3 {
		margin-bottom: 0.5rem;
		font-size: 1rem;
	}

	#history-list {
		margin: 0;
		padding-left: 1.15rem;
	}

	@media (max-width: 640px) {
		#randomiser-form {
			grid-template-columns: 1fr;
		}

		#generate-btn {
			width: 100%;
		}
	}
</style>

<script>
	(function () {
		var history = [];
		var form = document.getElementById('randomiser-form');
		var minInput = document.getElementById('min-value');
		var maxInput = document.getElementById('max-value');
		var resultValue = document.getElementById('result-value');
		var errorMessage = document.getElementById('randomiser-error');
		var historyList = document.getElementById('history-list');

		function renderHistory() {
			historyList.innerHTML = '';

			for (var i = 0; i < history.length; i += 1) {
				var item = document.createElement('li');
				item.textContent = String(history[i]);
				historyList.appendChild(item);
			}
		}

		function parseInteger(input) {
			return Number.parseInt(input.value, 10);
		}

		function setError(message) {
			errorMessage.textContent = message;
		}

		function generateRandomNumber(min, max) {
			return Math.floor(Math.random() * (max - min + 1)) + min;
		}

		form.addEventListener('submit', function (event) {
			event.preventDefault();

			var min = parseInteger(minInput);
			var max = parseInteger(maxInput);

			if (Number.isNaN(min) || Number.isNaN(max)) {
				setError('Enter valid whole numbers for minimum and maximum.');
				return;
			}

			if (min > max) {
				setError('Minimum must be less than or equal to maximum.');
				return;
			}

			setError('');
			var value = generateRandomNumber(min, max);
			resultValue.textContent = String(value);

			history.unshift(value);
			if (history.length > 10) {
				history = history.slice(0, 10);
			}

			renderHistory();
		});
	})();

</script>


