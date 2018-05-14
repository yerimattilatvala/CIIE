using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class PotionManager : MonoBehaviour {

    CharacterStats playerStats;
    public int healthUp;
	private bool used;

	void Start(){
		used = false;
	}


    void OnTriggerEnter(Collider col)
    {

        
		if (col.gameObject.tag == "Player") {
			if (used)
				return;
			else {
			used = true;
			Debug.Log ("Consumir pocion");
			Destroy (this.gameObject);
			playerStats = col.gameObject.GetComponentInChildren<CharacterStats> ();
			playerStats.IncreaseHealth (healthUp);


			}
		}
    }
}
