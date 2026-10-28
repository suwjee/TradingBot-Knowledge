import { buildReviewBody, reviewRuntime } from "./render.js";

const loading = document.getElementById("review-loading");
const app = document.getElementById("app");

function fail(message) {
  loading.innerHTML = `<p>${message}</p>`;
}

function renderReview(payload, snapshot) {
  if (!payload || typeof payload.directions !== "object") {
    fail("The received payload is not a valid indicator export.");
    return;
  }
  buildReviewBody(payload, snapshot)
    .then(({ hash, reviewId, body, bridgeData }) => {
      document.title = `Indicator Info · ${reviewId}`;
      document.body.dataset.payloadHash = hash;
      document.body.dataset.reviewId = reviewId;
      app.innerHTML = body;
      loading.remove();
      reviewRuntime(bridgeData);
    })
    .catch((error) => fail(`Could not render the review page: ${error.message}`));
}

async function loadCalculationReport() {
  const identity = location.pathname.replace(/^\/info\/?/, "");
  if (!identity) { fail("This report has no calculation identity."); return; }
  try {
    const response = await fetch(`/api/info/${identity}`, { cache: "no-store" });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Calculation report was not found");
    renderReview(result.payload, result.snapshot);
  } catch (error) {
    fail(`Could not load this calculation report: ${error.message}`);
  }
}

loadCalculationReport();
