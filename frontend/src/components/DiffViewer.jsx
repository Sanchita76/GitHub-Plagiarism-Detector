import { useEffect, useRef } from 'react';
import { renderDiff } from '../utils/diffRenderer';

export default function DiffViewer({ diffs }) {
  const ref = useRef();

  useEffect(() => {
    if (ref.current && diffs.length > 0) {
      const combinedDiff = diffs.map(d => d.diff).join('\n');
      renderDiff(ref.current, combinedDiff);
    }
  }, [diffs]);

  return <div ref={ref} className="overflow-auto mt-6" />;
}


