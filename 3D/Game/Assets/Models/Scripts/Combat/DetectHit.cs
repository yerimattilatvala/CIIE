using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DetectHit : MonoBehaviour {
	CharacterStats enemyStats;
	CharacterStats playerStats;
	AudioSource audioSource;

	private float volLowRange = .8f;
	private float volHighRange = 1.2f;

	void Start(){
		audioSource = GetComponent<AudioSource> ();
	}

	void OnTriggerEnter(Collider col){

		if (col.gameObject.tag == "hitMarker")
		{
			if (((EnemyAttackTimer)col.gameObject.GetComponent(typeof(EnemyAttackTimer))).canAttack()){
				playerStats = this.gameObject.GetComponentInChildren<CharacterStats> ();
				enemyStats = col.gameObject.GetComponentInParent<CharacterStats> ();
				Stat enemyDamage = enemyStats.damage;
				playerStats.TakeDamage (enemyDamage.getValue ());

				//Sonido de daño recibido
				audioSource.pitch = Random.Range (volLowRange, volHighRange);
				audioSource.Play();
			}
		}
	}
}
