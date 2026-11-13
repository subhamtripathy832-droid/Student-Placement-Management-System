function confirmApply() {
  return window.confirm("Submit your application for this job?");
}

document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    window.setTimeout(() => {
      alert.style.opacity = "0.85";
    }, 4000);
  });
});
