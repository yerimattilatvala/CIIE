using UnityEngine;

public class EnemyStats : CharacterStats {

	GameObject player;
	CharacterStats playerStats;

	void Start(){
		player = GameObject.FindWithTag ("Player");
		playerStats = player.GetComponent<CharacterStats> ();
	}


	void OnCollisionEnter(Collision collision){
		if (collision.gameObject.layer == 8) {
			this.TakeDamage (playerStats.damage.getValue());
			Destroy (collision.gameObject);
		}
	}
		
    
}
