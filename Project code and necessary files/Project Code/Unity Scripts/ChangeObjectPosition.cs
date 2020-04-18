using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

/// <summary>
/// Spawns two different images that depicts two different emotions, 
/// on the wall at different positions whenever the participant clicks
/// the space button and the positions, orientation, scale of different objects in the virtual 
/// reality environment are written to a text document.
/// </summary>

public class ChangeObjectPosition : MonoBehaviour
{
    
    /// <summary>
    /// GameObjects array whose positions are to be changed.
    /// </summary>
    public GameObject[] gameObjects;
    
    /// <summary>
    /// GameObject that represents the gaze point in the virtual reality environment.
    /// </summary>
    public GameObject hotSpot;

    /// <summary>
    /// Path to the text file into which the data is written.
    /// </summary>
    string path = "Assets/Files/DatasetDetails.txt";

    /// <summary>
    /// Writer object is used to write the data to the text document.
    /// </summary>
    StreamWriter writer;

    /// <summary>
    /// Counts the number of instances i.e., the nunber of times the participant clicks the space button.
    /// </summary>
    int counter = 0;

/**
 * Start method is called on the frame when a script is enabled just before any of the Update methods are called the first time.
 */
    void Start()
    {
       
    }

/**
 * Update method is called every frame, if the MonoBehaviour is enabled.
 */
    void Update()
    {
        hotSpot.SetActive(true);
        if (Input.GetKeyDown("space"))
        {
            //Debug.Log("Pressed space: ");
            ++counter;
            writer = new StreamWriter(path, true);
            DestroyAll("clone");
            gameObjects[0].transform.position = new Vector3(Random.Range(-850f, 810f)*0.01f, Random.Range(379f, -320f)*0.01f, -0.08f);
            gameObjects[1].transform.position = new Vector3(Random.Range(-850f, 810f)*0.01f, Random.Range(379f, -320f)*0.01f, -0.08f);
        

            writer.WriteLine("\n \n Set - " + counter);

            writer.WriteLine("Object - " + gameObjects[0].tag);
            writer.WriteLine("Position - " + gameObjects[0].transform.position);
            writer.WriteLine("Rotation - " + gameObjects[0].transform.rotation.eulerAngles);
            writer.WriteLine("Scale - " + gameObjects[0].transform.localScale + "\n ");

            writer.WriteLine("Object - " + gameObjects[1].tag);
            writer.WriteLine("Position - " + gameObjects[1].transform.position);
            writer.WriteLine("Rotation - " + gameObjects[1].transform.rotation.eulerAngles);
            writer.WriteLine("Scale - " + gameObjects[1].transform.localScale + "\n ");

            writer.Close();        }
    }

/**
 * DestroyAll method destroys all the game objects with a specific tag.
 @param[in] tag is used to identify the game objects and destroy them.
 @returns Nothing
 */
    void DestroyAll(string tag)
    {
        GameObject[] hotSpots = GameObject.FindGameObjectsWithTag(tag);
        for (int i = 0; i < hotSpots.Length; i++)
        {
            hotSpots[i].SetActive(false);  
            Destroy(hotSpots[i]);
        }
    }
}
