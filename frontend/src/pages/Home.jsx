import { useState } from 'react';
import axios from 'axios';
import DiffViewer from '../components/DiffViewer';

export default function Home() {
  const [url, setUrl] = useState('');
  const [res, setRes] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const r = await axios.post('http://localhost:8000/analyze', {
  repo_url: url,
});

    setRes(r.data);
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4"></h1>
      <form onSubmit={handleSubmit} className="mb-6">
        <input
          type="text"
          placeholder="Enter GitHub Repository URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border p-2 w-96"
        />
        <button type="submit" className="ml-2 bg-blue-600 text-white px-4 py-2">Check</button>
      </form>

      {res && (
        <div>
          <p><strong>Commit Date Range:</strong> {res.commit_start} → {res.commit_end}</p>
          {res.match_repo && (
            <p><strong>Matched Original Repo:</strong> <a href={res.match_repo} target="_blank" rel="noopener noreferrer" className="text-blue-600">{res.match_repo}</a></p>
          )}
          <p><strong>Semantic Similarity:</strong> {res.similarity_score}</p>
          <p><strong>Plagiarism Score:</strong> {res.plagiarism_score}%</p>
          {res.diffs && <DiffViewer diffs={res.diffs} />}
        </div>
      )}
    </div>
  );
}
