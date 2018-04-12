using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DetectCollision: MonoBehaviour {

    void OnTriggerEnter(Collider col)
    {
        if (col.gameObject.tag == "potion")
        {
            Destroy(col.gameObject);

            //Dar vida
        }
    }
}
