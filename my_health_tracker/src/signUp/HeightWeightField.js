function HeightWeightField({setWeight, setHeight}) {
    return (
        <div className="row height-weight">
            <div className="col">
                <label htmlFor="height" className="form-label">Height</label>
                <input type="text" className="form-control" id="height" placeholder="Height" required onChange={(e) => setHeight(e.target.value)}/>
            </div>
            <div className="col">
                <label htmlFor="weight" className="form-label">Weight</label>
                <input type="text" className="form-control" id="weight" placeholder="Weight" required onChange={(e) => setWeight(e.target.value)}/>
            </div>
        </div>
    );
}

export default HeightWeightField;