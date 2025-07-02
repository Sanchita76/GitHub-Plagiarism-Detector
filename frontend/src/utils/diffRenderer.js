// src/utils/diffRenderer.js
import { Diff2HtmlUI } from 'diff2html/lib/ui/js/diff2html-ui.js';
import 'diff2html/bundles/css/diff2html.min.css';

export function renderDiff(container, diffString) {
  const ui = new Diff2HtmlUI(container, diffString, {
    drawFileList: true,
    matching: 'lines',
    outputFormat: 'side-by-side',
  });
  ui.draw();
  ui.highlightCode();
}
