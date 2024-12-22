import './App.css'
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import { AiTwotoneExperiment } from "react-icons/ai";
import ExperimentsOverview from './components/ExperimentsOverview';
import ExperimentForm from './components/ExperimentForm';
import Login from './components/Login';
import { useState } from 'react';
import { FiLogOut } from 'react-icons/fi';

function App() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [jwt, setJwt] = useState<string | null>(localStorage.getItem('jwt'));

  const handleLogin = (newJwt: string) => {
    localStorage.setItem('jwt', newJwt);
    setJwt(newJwt);
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt');
    setJwt(null);
  };

  if (!jwt) {
    return <Login onLogin={handleLogin} />;
  }

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
          <div className={`flex flex-col gap-5 transition ${isCollapsed ? 'p-2' : 'p-4'}`}>
            <a href="/experiments"
              className={`transition text-blue-500 hover:bg-gray-100 rounded flex items-center gap-2`}
              title="Experiments">
                <AiTwotoneExperiment  className="block min-w-5 h-5" />
              <div className="flex-shrink-1">
                {!isCollapsed && 'Experiments'}
              </div>
            </a>
            <button 
              onClick={handleLogout}
              className="transition text-red-500 hover:bg-gray-100 rounded flex items-center gap-2"
            >
                <FiLogOut  className="block min-w-5 h-5" />
              <div className="flex-shrink-1">
                {!isCollapsed && 'Logout'}
              </div>
            </button>
          </div>
        </nav>
        <div className={`absolute right-0 bg-gray-100 min-h-screen p-4 transition max-w-full ${isCollapsed ? 'left-16' : 'left-40 xl:left-48'}`}>
          <h1 className="text-4xl font-bold mb-8">
            MUSCLE forms
          </h1>
          <Routes>
            <Route path="/experiments/:id" element={<ExperimentForm jwt={jwt} />} />
            <Route path={'/experiments'} element={<ExperimentsOverview jwt={jwt} />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
