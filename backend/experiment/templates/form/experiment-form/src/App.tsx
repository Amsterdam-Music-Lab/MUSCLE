import './App.css'
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import ExperimentsOverview from './components/ExperimentsOverview';
import ExperimentForm from './components/ExperimentForm';
import { useState } from 'react';

function App() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <Router>
      <div className="flex">
        <nav className={`h-screen bg-white shadow-lg transition-all ${isCollapsed ? 'w-16' : 'w-64'}`}>
          <button 
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="w-full p-4 text-left hover:bg-gray-100"
          >
            {isCollapsed ? '→' : '←'}
          </button>
          <div className="p-4">
            <a href="/experiments" className="block text-blue-500 hover:bg-gray-100 p-2 rounded">
              {isCollapsed ? 'E' : 'Experiments'}
            </a>
          </div>
        </nav>
        <div className="flex-1 bg-gray-100 min-h-screen p-4">
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
