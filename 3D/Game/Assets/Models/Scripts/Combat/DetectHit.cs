using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DetectHit : MonoBehaviour {
	CharacterStats enemyStats;
	CharacterStats playerStats;

	void OnTriggerEnter(Collider col){

		if (col.gameObject.tag == "hitMarker")
		{
			if (((EnemyAttackTimer)col.gameObject.GetComponent(typeof(EnemyAttackTimer))).canAttack()){
				playerStats = this.gameObject.GetComponentInChildren<CharacterStats> ();
				enemyStats = col.gameObject.GetComponentInParent<CharacterStats> ();
				Stat enemyDamage = enemyStats.damage;
				playerStats.TakeDamage (enemyDamage.getValue ());
			}
		}
	}
}
