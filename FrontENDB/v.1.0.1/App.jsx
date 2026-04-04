import { useEffect, useState } from "react";

// Base URL for API (injected via Vite environment variables)
// Example: http://localhost:8000
const API_BASE = import.meta.env.VITE_API_BASE;

//The option limits for inputs into database
const ITEM_TYPES = ["Pants", "Shirt", "Dress", "Socks"];
const COLOURS = ["Blue", "Black", "White", "Yellow", "Red", "Grey", "Brown", "Green", "Pink"]
const SIZES = ["Small", "Medium", "Large", "XLarge"]


export default function App() {
  //the react state variable for drop down menu for the front end set itemtype "Dress" as the default option
  const [itemType, setItemType] = useState("Dress");

  //the react state variable For the checkmark menu for the front end set colours, no defaults can click multiples as an array
  const [colours, setColours] = useState([]);

  //the react state variable For the radio button size for the front end setSize, no defaults in case they forget to click on it shouldn't be defaulted to a size that isn't correct
  const [size, setSize] = useState("");

  //the react state for the list of stock items from the backend
  const [items, setItems] = useState([]);

  // State: total press count from backend will eventually by changed to track amount of items
  const [count, setCount] = useState(0);

  // State: loading flag to prevent double submissions + update UI
  const [loading, setLoading] = useState(false);

  //the react state for the errors
  const [error, setError] = useState("");


  // Get the items and total item count from the backend
  const loadItems = async () => {

    //Gets the full list of database of stock items from backend
    const itemsRes = await fetch(`${API_BASE}/items`);

    //Gets the total count of databased items from the backend
    const countRes = await fetch(`${API_BASE}/items/count`);

    //error checking of both
    if (!itemsRes.ok) {
      throw new Error("Could not load inventory items from the backend");
    }
    if (!countRes.ok) {
      throw new Error("Could not load inventory count from the backend");
    }

    //converts the response from /items into JSON
    const itemsData = await itemsRes.json();

    //converts the reponse from /items/count into JSON
    const countData = await countRes.json();

    //storing the returned stock items in React so they can be shown in table
    setItems(itemsData);

    //storing the returned item count in react so it can be shown on the frontend page
    setCount(countData.count);
  };

  //update the current list of selected colours
  const toggleColour = (colour) => {
    setColours((current) => {

      //checking if the clicked colour has already been selected
      const alreadySelected = current.includes(colour);

      //If the colour has already been selected remove it to ensure no duplicate colours in the array
      if (alreadySelected) {
        const updatedColours = current.filter((existingColour) => existingColour !== colour);
        return updatedColours;
      }
      else {
        // if the colour is not selected before then add it to array
        const updatedColours = [...current, colour];
        return updatedColours;
      }
    });
  };

  //This function handles when the form is submitted
  const handleSubmit = async (event) => {

    //This will prevent the page from reloading when the form is submitted
    event.preventDefault();

    //clear out any old errors before checking again for any errors
    setError("");

    //if the colours array length is zero there was an error with the submission
    if (colours.length === 0) {
      setError("You need to checkmark atleast one colour for the item");

      //since there was an error stops the form from being submitted
      return;
    }

    //turns on the loading state so the button can't be clicked more than once
    setLoading(true);
    try {
      //Here creates an item object that has the stock data to send to backend
      const newItem = { item_type: itemType, colours, size };

      //Send a post request to the backend /items route with the new item object as JSON
      const response = await fetch(`${API_BASE}/items`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(newItem) });


      //so if the backend response was not a success we thow an error to show it didn't save
      if (!response.ok) {
        throw new Error("This item could not be saved to the database");
      }

      //the database items and count is reloaded after a successful save
      await loadItems();

      //reseting the defaults on the form
      setItemType("Dress");
      setColours([]);
      setSize("");
      //if there was an issue during the save throw an error message
    } catch (err) {
      setError(err.message || "Error couldn't save to database");
    } finally {
      //ensure the botton can be clicked by turning off loading
      setLoading(false);
    }
  };

  //Once the page first loads. *This code then Runs
  useEffect(() => {

    //function to load saved items from the backend
    const getItems = async () => {
      try {
        //trying to load items and count
        await loadItems();
      } catch {
        //if there is an error here then there is an issue with frontend -backend connection
        setError("Can't connect to the backend");
      }
    };

    //calling the function to get the items from the backend
    getItems();
  }, []);

  return (
    <div className="page">
      <div className="card">
        <h1>Button Press Logger</h1>

        {/* Display current press count */}
        <p>Total presses: {count}</p>

        {/* Button triggers press event */}
        {/* Disabled while request is in progress */}
        <button onClick={handlePress} disabled={loading}>
          {loading ? "Saving..." : "Press Me"}
        </button>
      </div>
    </div>
  );
}