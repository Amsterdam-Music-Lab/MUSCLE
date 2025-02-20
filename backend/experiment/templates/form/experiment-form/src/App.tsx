import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
} from "react-router-dom";
import { AiFillQuestionCircle, AiTwotoneExperiment } from "react-icons/ai";
import ExperimentsOverview from './components/ExperimentsOverview';
import ExperimentForm from './components/ExperimentForm';
import Login from './components/Login';
import { useState } from 'react';
import { FiLogOut } from 'react-icons/fi';
import { Toasts } from './components/Toasts';
import useBoundStore from "./utils/store";
import QuestionsOverview from './components/QuestionsOverview';
import QuestionFormPage from './pages/QuestionFormPage';

function App() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const jwt = useBoundStore(state => state.jwt);
  const setJwt = useBoundStore(state => state.setJwt);

  const handleLogin = (newJwt: string) => {
    setJwt(newJwt);
  };

  const handleLogout = () => {
    setJwt(null);
  };

  if (!jwt) {
    return <Login onLogin={handleLogin} />;
  } else {
    try {
      const payload = JSON.parse(atob(jwt.split('.')[1]));
      if (payload.exp && Date.now() >= payload.exp * 1000) {
        handleLogout();
        return <Login onLogin={handleLogin} />;
      }
    } catch (error) {
      handleLogout();
      return <Login onLogin={handleLogin} />;
    }
  }

  return (
    <>
      <Router>
        <div className="flex relative">
          <nav className={`flex flex-col fixed h-screen bg-white shadow-lg transition ${isCollapsed ? 'w-16' : 'w-40 xl:w-48'}`}>
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="w-full p-4 text-left hover:bg-gray-100"
            >
              {isCollapsed ? '→' : '←'}
            </button>
            <div className={`flex flex-col justify-between gap-5 transition ${isCollapsed ? 'p-2' : 'p-4'}`}>
              <h1 className={`text-left text-lg font-rajdhani font-bold ${isCollapsed ? 'hidden' : ''}`}>
                MUSCLE Dashboard
              </h1>
              <Link to="/experiments"
                className={`transition text-blue-500 hover:bg-gray-100 rounded flex items-center gap-2`}
                title="Experiments">
                <AiTwotoneExperiment className="block min-w-5 h-5" />
                <div className="flex-shrink-1">
                  {!isCollapsed && 'Experiments'}
                </div>
              </Link>
              <Link to="/questions"
                className="transition text-blue-500 hover:bg-gray-100 rounded flex items-center gap-2"
                title="Questions">
                <AiFillQuestionCircle className="block min-w-5 h-5" />
                <div className="flex-shrink-1">
                  {!isCollapsed && 'Questions'}
                </div>
              </Link>
              <button
                onClick={handleLogout}
                className="transition text-red-500 hover:bg-gray-100 rounded flex items-center gap-2"
              >
                <FiLogOut className="block min-w-5 h-5" />
                <div className="flex-shrink-1">
                  {!isCollapsed && 'Logout'}
                </div>
              </button>

            </div>

          </nav>
          <div className={`absolute right-0 bg-gray-100 min-h-screen p-4 transition max-w-full ${isCollapsed ? 'left-16' : 'left-40 xl:left-48'}`}>
            <Routes>
              <Route path="/experiments" element={<ExperimentsOverview />} />
              <Route path="/experiments/:id/*" element={<ExperimentForm />} />
              <Route path="/questions" element={<QuestionsOverview />} />
              <Route path="/questions/new" element={<QuestionFormPage />} />
              <Route path="/questions/:id/edit" element={<QuestionFormPage />} />
              <Route path="/" element={<ExperimentsOverview />} />
            </Routes>
          </div>
        </div>
      </Router>
      <Toasts />
    </>
  )
}

export default App
