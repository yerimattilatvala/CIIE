using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class DetectCollisionObjects: MonoBehaviour {

    public Transform origin;                                    // origin to aim for
    CharacterStats objectStats;
    CharacterStats playerStats;
    public float distance = 20f;

    void OnTriggerEnter(Collider col)
    {
        if (origin != null)
            distance = Vector3.Distance(origin.position, transform.position);

        if (col.gameObject.tag == "potion")
        {
            Debug.Log("Colision pocion");
            Destroy(col.gameObject);
            objectStats = col.gameObject.GetComponent<CharacterStats>();
            Stat life = objectStats.life;

            playerStats = origin.GetComponent<CharacterStats>();
            playerStats.IncreaseHealth(life.getValue());


        }
    }
}
