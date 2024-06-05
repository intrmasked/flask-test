from datetime import datetime
import json
from flask import Flask,jsonify,request,abort
from threading import Thread   
import uuid
from crew import CompanyResearchCrew
from job_manager import Event, append_event, jobs_lock, jobs
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})




def kickoff_crew(job_id:str, companies: list[str], positions: list[str]):
    try: 
        company_research_crew=CompanyResearchCrew(job_id)
        company_research_crew.setup_crew(companies,positions)
        results = company_research_crew.kickoff()
    except Exception as e:
        print(f"error: {str(e)}")
        append_event(job_id, f"Error: {str(e)}")
        with jobs_lock:
            jobs[job_id].status = "Error"
            jobs[job_id].results = str(e)
        return str(e)
    
    with jobs_lock:
        jobs[job_id].status = "Complete"
        jobs[job_id].results = results
        jobs[job_id].events.append(Event(timestamp=datetime.now(), data="Crew complete"))



@app.route('/api/crew', methods=['POST'])
def run_crew():
    data = request.json

    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description='companies and positions are required')

    
    job_id = str(uuid.uuid4())
    companies = data['companies']
    positions = data['positions']

    thread = Thread(target=kickoff_crew, args=(job_id, companies, positions))
    thread.start()

    return jsonify({'job_id': job_id})


@app.route('/api/crew/<job_id>', methods=['GET'])

def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")

     # Parse the job.result string into a JSON object
    try:
        result_json = json.loads(job.results)
    except json.JSONDecodeError:
        # If parsing fails, set result_json to the original job.result string
        result_json = job.results

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })



@app.route('/', methods=['GET'])
# just do a hello world
def hello():
    return "Hello, World!"


   



    


if __name__ == '__main__':
    app.run(debug=True,port=5000)