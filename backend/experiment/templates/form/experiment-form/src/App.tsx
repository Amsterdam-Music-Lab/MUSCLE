import './App.css'
import ExperimentForm from './components/ExperimentForm'
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";

function App() {
  return (
    <>
      <h1 className="text-4xl font-bold text-center">
        MUSCLE forms
      </h1>
      <nav className="flex justify-center space-x-4 mt-8">
        <a href="/experiments" className="text-blue-500">Create Experiment</a>
      </nav>
      <div>
        <Router>
          <Routes>
            {/* Request reload for given participant */}
            <Route path={'/experiments'} element={<ExperimentForm />} />
          </Routes>
        </Router >
      </div>

    </>
  )
}

export default App
