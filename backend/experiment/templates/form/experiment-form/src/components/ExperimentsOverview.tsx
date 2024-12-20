import { createEntityUrl } from "../config";
import useFetch from "../hooks/useFetch";
import { Link } from "react-router-dom";
import Page from "./Page";

type Experiment = {
  id?: number;
  slug: string;
  active: boolean;
}

const url = createEntityUrl('experiments');

const ExperimentsOverview = () => {
  const [experiments, error, loading, fetchData] = useFetch<Experiment[]>(url);
  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this experiment?')) {
      try {
        await fetch(`${url}/${id}/`, { method: 'DELETE' });
        // Refresh the page or update the list
        fetchData();
      } catch (error) {
        console.error('Error deleting experiment:', error);
      }
    }
  };

  if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;
  const loadingClass = loading ? 'opacity-50 pointer-events-none' : '';

  async function onCreateExperiment() {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ slug: 'new-experiment', active: false }),
    });
    if (response.ok) {
      fetchData();
      // navigate to the new experiment
      const id = (await response.json()).id;
      window.location.href = `/experiments/${id}`;
    } else {
      console.error('Failed to create experiment:', response);
    }
  }


  return (
    <Page title="Experiments">
      <div className={`${loadingClass}`}>
        <div className="flex justify-end mb-4">
          <button
            onClick={onCreateExperiment}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            New Experiment
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full bg-white shadow-md rounded">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Slug</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {experiments?.map((experiment) => (
                <tr key={experiment.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-left whitespace-nowrap">{experiment.id}</td>
                  <td className="px-6 py-4 text-left whitespace-nowrap">{experiment.slug}</td>
                  <td className="px-6 py-4 text-left whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${experiment.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                      {experiment.active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Link
                      to={`/experiments/${experiment.id}`}
                      className="text-indigo-600 hover:text-indigo-900 mr-4"
                    >
                      Edit
                    </Link>
                    <button
                      onClick={() => experiment.id && handleDelete(experiment.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Page>
  );
};

export default ExperimentsOverview;
