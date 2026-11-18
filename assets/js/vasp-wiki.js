/* Add copy controls without changing the archived code text. */
(function () {
  "use strict";
  var status = document.querySelector(".wiki-copy-status");
  var statusTimer;
  function announce(message) {
    status.textContent = message;
    clearTimeout(statusTimer);
    statusTimer = setTimeout(function () { status.textContent = ""; }, 3500);
  }
  document.querySelectorAll(".wiki-content .highlight").forEach(function (block) {
    var code = block.querySelector("pre code");
    if (!code) return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "wiki-copy";
    button.textContent = "Copy code";
    button.setAttribute("aria-label", "Copy archived code example");
    button.addEventListener("click", async function () {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = "Copied";
        announce("Code copied. Review historical instructions before use.");
        setTimeout(function () { button.textContent = "Copy code"; }, 2000);
      } catch (error) {
        var selection = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(code);
        selection.removeAllRanges();
        selection.addRange(range);
        announce("Copy is unavailable. Code selected; use your keyboard to copy.");
      }
    });
    block.appendChild(button);
  });
})();
