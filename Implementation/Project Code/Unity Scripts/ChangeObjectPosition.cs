using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ChangeObjectPosition : MonoBehaviour
{
    public GameObject[] gameObjects;
    //public Text Counter;
    public GameObject hotSpot;
    Vector3[] positions;
    

    string path = "Assets/Files/DatasetDetails.txt";
    string path2 = "Assets/Files/GazeDetails.txt";
    public StreamWriter writer, writer2;
    int i = 199;
    AttentionPointsPlotter app;

    // Start is called before the first frame update
    void Start()
    {
        app = new AttentionPointsPlotter();
    }

    // Update is called once per frame
    void Update()
    {
        hotSpot.SetActive(true);
        if (Input.GetKeyDown("space"))
        {
            Debug.Log("Pressed space: ");
            ++i;
            writer = new StreamWriter(path, true);
            
            DestroyAll("clone");

            gameObjects[3].GetComponent<UnityEngine.UI.Text>().text = i.ToString();
            gameObjects[0].transform.position = new Vector3(Random.Range(-1035f, 800f)*0.01f, Random.Range(350f, 150f)*0.01f, Random.Range(-50f, -15f) * 0.01f);
            gameObjects[1].transform.position = new Vector3(Random.Range(-1035f, 800f)*0.01f, Random.Range(350f, 150f) *0.01f, Random.Range(-50f, -15f) * 0.01f);



            // The following lines of codew write the data to a text file
            
            writer.WriteLine("\n \n Set - " + i);

            writer.WriteLine("Object - " + gameObjects[0].tag);
            writer.WriteLine("Position - " + gameObjects[0].transform.position);
            writer.WriteLine("Rotation - " + gameObjects[0].transform.rotation.eulerAngles);
            writer.WriteLine("Scale - " + gameObjects[0].transform.localScale + "\n ");

            writer.WriteLine("Object - " + gameObjects[1].tag);
            writer.WriteLine("Position - " + gameObjects[1].transform.position);
            writer.WriteLine("Rotation - " + gameObjects[1].transform.rotation.eulerAngles);
            writer.WriteLine("Scale - " + gameObjects[1].transform.localScale + "\n ");

            writer.WriteLine("Gaze Points:" + gameObjects[2].GetComponent<AttentionPointsPlotter>().gaze_point);
            
            writer.WriteLine("Camera position-:" + gameObjects[4].transform.position);


            writer.Close();
        }
    }

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
