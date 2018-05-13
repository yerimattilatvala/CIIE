using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class PotionManager : MonoBehaviour {

    CharacterStats playerStats;
    public int healthUp;

    void OnTriggerEnter(Collider col)
    {
        
        if (col.gameObject.tag == "Player")
        {
            Debug.Log("Consumir pocion");
            Destroy(this.gameObject);
            playerStats = col.gameObject.GetComponentInChildren<CharacterStats>();
            playerStats.IncreaseHealth(healthUp);


        }
    }
}
