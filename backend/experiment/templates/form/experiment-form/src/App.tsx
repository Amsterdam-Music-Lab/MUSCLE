import './App.css'
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import ExperimentsOverview from './components/ExperimentsOverview';
import ExperimentForm from './components/ExperimentForm';

function App() {
  return (
    <div className="w-full bg-gray-100 min-h-screen p-4">
      <h1 className="text-4xl font-bold text-center">
        MUSCLE forms
      </h1>
      <nav className="flex justify-center space-x-4 mt-8">
        <a href="/experiments" className="text-blue-500">Experiments</a>
      </nav>
      <div>
        <Router>
          <Routes>
            <Route path="/experiments/:id" element={<ExperimentForm />} />
            <Route path={'/experiments'} element={<ExperimentsOverview />} />
          </Routes>
        </Router >
      </div>

    </div>
  )
}

export default App
