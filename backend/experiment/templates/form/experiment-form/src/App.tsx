import './App.css'
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import { AiTwotoneExperiment } from "react-icons/ai";
import ExperimentsOverview from './components/ExperimentsOverview';
import ExperimentForm from './components/ExperimentForm';
import { useState } from 'react';

function App() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <Router>
      <div className="flex relative">
        <nav className={`fixed h-screen bg-white shadow-lg transition ${isCollapsed ? 'w-16' : 'w-40 xl:w-48'}`}>
          <button 
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="w-full p-4 text-left hover:bg-gray-100"
          >
            {isCollapsed ? '→' : '←'}
          </button>
          <div className={`transition ${isCollapsed ? 'p-2' : 'p-4'}`}>
            <a href="/experiments"
              className={`transition text-blue-500 hover:bg-gray-100 rounded flex items-center gap-2 ${isCollapsed ? 'p-1' : 'p-2'}`}
              title="Experiments">
              <AiTwotoneExperiment className="w-5 h-5" />
              {!isCollapsed && 'Experiments'}
            </a>
          </div>
        </nav>
        <div className={`absolute right-0 bg-gray-100 min-h-screen p-4 transition max-w-full ${isCollapsed ? 'left-16' : 'left-40 xl:left-48'}`}>
          <h1 className="text-4xl font-bold mb-8">
            MUSCLE forms
          </h1>
          <Routes>
            <Route path="/experiments/:id" element={<ExperimentForm />} />
            <Route path={'/experiments'} element={<ExperimentsOverview />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
