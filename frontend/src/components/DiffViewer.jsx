import 'diff2html/bundles/css/diff2html.min.css';
import Diff2Html from 'diff2html';
import { useEffect, useRef } from 'react';

export default function DiffViewer({ diffs }) {
  const ref = useRef();

  useEffect(() => {
    if (ref.current && diffs.length > 0) {
      const fullDiff = diffs.map(d => d.diff).join('\n');
      ref.current.innerHTML = Diff2Html.getPrettyHtml(fullDiff, {
        inputFormat: 'diff',
        showFiles: true,
        matching: 'lines',
        outputFormat: 'side-by-side',
      });
    }
  }, [diffs]);

  return <div ref={ref} className="overflow-auto mt-6" />;
}

