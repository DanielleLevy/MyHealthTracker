import React, { useState, useEffect } from "react";
import axios from "axios";
import "./LifestyleQuestionnaire.css";

function LifestyleQuestionnaire({ username,  }) {
    const [lifestyleData, setLifestyleData] = useState();
    const [formData, setFormData] = useState({
    marital_status: "",
    education_levels: "",
    children: "",
    physical_activity: "",
    work: "",
    dietary_habit: "",
    sleep_pattern: "",
    drinking: "",
    smoking: "",
  });

  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:5001/api/get_lifestyle_info?username=${username}`)
      .then(response => {
        setFormData(response.data);
        setLifestyleData(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching lifestyle information:", error);
        setLoading(false);
      });
  }, [username, setLifestyleData]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdate = (e) => {
    e.preventDefault();
    axios.post("http://localhost:5001/api/update_lifestyle_info", {
      username: username,
      ...formData,
    })
      .then(() => {
        alert("Lifestyle information updated successfully!");
        setLifestyleData((prev) => ({ ...prev, ...formData }));
        setIsEditing(false);
      })
      .catch((error) => {
        console.error("Error updating lifestyle information:", error);
        alert("Failed to update lifestyle information.");
      });
  };

  if (loading) return <p>Loading lifestyle information...</p>;

  return (
    <div className="lifestyle-container">
      <h2>Lifestyle Questionnaire</h2>
      <button className="edit-btn" onClick={() => setIsEditing(!isEditing)}>
        {isEditing ? "Cancel" : "Edit Lifestyle"}
      </button>
      <form onSubmit={handleUpdate} className="lifestyle-form">
      <div className="lifestyle-input-group">
      <i className="fas fa-heart icon"></i>
          <select name="marital_status" value={formData.marital_status} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select Marital Status</option>
            <option value={1}>Single</option>
            <option value={2}>Married</option>
            <option value={3}>Divorced</option>
            <option value={4}>Widowed</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-user-graduate icon"></i>
          <select name="education_levels" value={formData.education_levels} onChange={handleInputChange} disabled={!isEditing} required>
          <option value={""}>Select Education Level</option>
            <option value={1}>High School</option>
            <option value={2}>Associate Degree</option>
            <option value={3}>Bachelor's Degree</option>
            <option value={4}>Master's Degree</option>
            <option value={5}>PhD</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-child icon"></i>
          <input type="number" name="children" value={formData.children} placeholder="Choose number of children" onChange={handleInputChange} disabled={!isEditing} min="0" required/>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-running icon"></i>
          <select name="physical_activity" value={formData.physical_activity} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select Physical Activity</option>
            <option value={1}>Sedentary</option>
            <option value={2}>Moderate</option>
            <option value={3}>Active</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-briefcase icon"></i>
          <select name="work" value={formData.work} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select Work Status</option>
            <option value={0}>Unemployed</option>
            <option value={1}>Employed</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-utensils icon"></i>
          <select name="dietary_habit" value={formData.dietary_habit} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select Dietary Habit</option>
            <option value={1}>Healthy</option>
            <option value={2}>Moderate</option>
            <option value={3}>Unhealthy</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-bed icon"></i>
          <select name="sleep_pattern" value={formData.sleep_pattern} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select Sleep Pattern</option>
            <option value={1}>Good</option>
            <option value={2}>Fair</option>
            <option value={3}>Poor</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-wine-glass icon"></i>
          <select name="drinking" value={formData.drinking} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select drinking status</option>
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>

        <div className="lifestyle-input-group">
        <i className="fas fa-smoking icon"></i>
          <select name="smoking" value={formData.smoking} onChange={handleInputChange} disabled={!isEditing} required>
            <option value={""}>Select Smoking Status</option>
            <option value={1}>Don't Smoke</option>
            <option value={2}>Smoked Before, but Quit</option>
            <option value={3}>Currently Smokes</option>
          </select>
        </div>

        {isEditing && (
          <button type="submit" className="btn-update">Save Changes</button>
        )}
      </form>
    </div>
  );
}

export default LifestyleQuestionnaire;
