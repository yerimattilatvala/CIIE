using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DmgUpPotionController : MonoBehaviour {

	CharacterStats playerStats;
	public int dmgUp;
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

			Debug.Log ("Consumir pocion Daño");
			Destroy (this.gameObject);
			playerStats = col.gameObject.GetComponentInChildren<CharacterStats> ();
			playerStats.IncreaseDamage (dmgUp);


			} 
		}
	}


}
