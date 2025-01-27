import React, { useState } from "react";
import axios from "axios";
import "./PersonalInformation.css";

function PersonalInformation({ userData, setUserData }) {
  const [formData, setFormData] = useState({
    age: userData?.age || "",
    height: userData?.height || "",
    weight: userData?.weight || "",
  });

  const [isEditing, setIsEditing] = useState(false); // מצב עריכה

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdate = (e) => {
    e.preventDefault();

    axios.post("http://localhost:5001/api/update_user_info", {
      username: userData.username,
      age: formData.age,
      height: formData.height,
      weight: formData.weight,
    })
      .then(() => {
        alert("Personal information updated successfully!");
        setUserData((prev) => ({
          ...prev,
          age: formData.age,
          height: formData.height,
          weight: formData.weight,
          BMI: calculateBMI(formData.height, formData.weight),
        }));
        setIsEditing(false); 
      })
      .catch((error) => {
        console.error("Error updating personal information:", error);
        alert("Failed to update personal information.");
      });
  };

  const calculateBMI = (height, weight) => {
    if (!height || !weight) return "N/A";
    const heightInMeters = height / 100;
    return (weight / (heightInMeters * heightInMeters)).toFixed(2);
  };

  return (
    <div className="personal-info-container">
      <h2>Personal Information</h2>
      {userData ? (
        <div className="user-info">
          <p><strong>Username:</strong> {userData.username}</p>
          <p><strong>Gender:</strong> {userData.gender === 1 ? "Male" : userData.gender === 2 ? "Female" : "Other"}</p>
          <p><strong>BMI:</strong> {userData.BMI}</p>

          <button className="edit-btn" onClick={() => setIsEditing(!isEditing)}>
            <i className="fas fa-user-edit"></i> {isEditing ? "Cancel" : "Edit Details"}
          </button>

          <form onSubmit={handleUpdate} className="update-form">
          <div className="input-group-info">
            <i className="fas fa-calendar-alt icon"></i>
            <span className="input-label-info">Age:</span>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              placeholder="Age"
              disabled={!isEditing}
              required
            />
          </div>



            <div className="input-group-info">
              <i className="fas fa-ruler-vertical icon"></i>
              <span className="input-label-info">Height:</span>
              <input
                type="number"
                name="height"
                value={formData.height}
                onChange={handleInputChange}
                placeholder="Height (cm)"
                disabled={!isEditing}
                required
              />
            </div>

            <div className="input-group-info">
              <i className="fas fa-weight icon-info"></i>
              <span className="input-label-info">Weight:</span>

              <input
                type="number"
                name="weight"
                value={formData.weight}
                onChange={handleInputChange}
                placeholder="Weight (kg)"
                disabled={!isEditing}
                required
              />
            </div>

            {isEditing && (
              <button type="submit" className="btn-update">
                <i className="fas fa-save"></i> Update
              </button>
            )}
          </form>
        </div>
      ) : (
        <p>Loading personal information...</p>
      )}

    </div>
  );
}

export default PersonalInformation;
