using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Position of the camera is controlled based on the player's position. 
/// </summary>

public class CameraController : MonoBehaviour
{
    /// <summary>
    /// Reference GameObject to change the position of camera. 
    /// </summary>
    public GameObject player;
    
    /// <summary>
    /// Difference between the position of reference gameobject and camera. 
    /// </summary>
    private Vector3 offset;


/**
 * Start method is called on the frame when a script is enabled just before any of the Update methods are called the first time.
 */
    void Start()
    {
        offset = transform.position - player.transform.position;
    }


/**
 * Update method is called every frame, if the MonoBehaviour is enabled.
 */
    void Update()
    {
        // Transforms the position of the camera as per the position of the plahyer game object

        transform.position = player.transform.position + offset;
    }
}
